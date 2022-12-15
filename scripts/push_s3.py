import argparse
from datetime import datetime, timezone
import boto3
import fnmatch
import itertools
import os
import stat
import json
from botocore.exceptions import ClientError


def recursive_list_bucket(s3, bucket_id):
    bucket_contents = []
    continuation_token = None

    while True:
        params = {
            "Bucket": bucket_id,
            **({"ContinuationToken": continuation_token} if continuation_token else {}),
        }
        bucket_listing_response = s3.list_objects_v2(**params)

        bucket_contents += [
            (l["Key"], l["LastModified"]) for l in bucket_listing_response["Contents"]
        ]

        if not bucket_listing_response["IsTruncated"]:
            break

        continuation_token = bucket_listing_response["NextContinuationToken"]

    return bucket_contents


def upload_file(s3, root_path, key, bucket):
    try:
        print(f"Uploading {key} to s3")
        response = s3.upload_file(os.path.join(root_path, key), bucket, key)

        # Touch the local file so we know not to upload it again
        os.utime(os.path.join(root_path, key))

    except ClientError as e:
        print(f"Error uploading {key}")
        print(e)
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cfg",
        type=str,
        help="The S3 configuration file (keys: bucket_id, access_key_id, secret_access_key)",
    )
    parser.add_argument("pdfs", type=str, help="Path to pdfs")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't change anything, just print what would happen",
    )
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    with open(args.cfg) as f:
        cfg = json.load(f)

    local_paths = list(
        itertools.chain.from_iterable(
            [
                [
                    os.path.relpath(os.path.join(root, fname), args.pdfs)
                    for fname in fnmatch.filter(fnames, "*.pdf")
                ]
                for root, dirnames, fnames in os.walk(args.pdfs)
            ]
        )
    )
    local_paths_with_mtimes = [
        (
            p,
            datetime.fromtimestamp(
                os.stat(os.path.join(args.pdfs, p))[stat.ST_MTIME], tz=timezone.utc
            ),
        )
        for p in local_paths
    ]

    s3 = boto3.client(
        "s3",
        aws_access_key_id=cfg["access_key_id"],
        aws_secret_access_key=cfg["secret_access_key"],
    )
    bucket_listing = recursive_list_bucket(s3, cfg["bucket_id"])
    bucket_listing = [
        (key, mtime) for key, mtime in bucket_listing if fnmatch.fnmatch(key, "*.pdf")
    ]

    bucket_listing = dict(bucket_listing)
    local_paths_with_mtimes = dict(local_paths_with_mtimes)

    keys_in_s3_not_in_local = list(
        set(list(bucket_listing.keys())) - set(list(local_paths_with_mtimes.keys()))
    )
    keys_in_local_not_in_s3 = list(
        set(list(local_paths_with_mtimes.keys())) - set(list(bucket_listing.keys()))
    )
    keys_that_need_updating_on_s3 = [
        (key, mtime, bucket_listing[key])
        for key, mtime in local_paths_with_mtimes.items()
        if key in bucket_listing and mtime > bucket_listing[key]
    ]
    keys_that_need_updating_on_local = [
        (key, mtime, local_paths_with_mtimes[key])
        for key, mtime in bucket_listing.items()
        if key in local_paths_with_mtimes and mtime > local_paths_with_mtimes[key]
    ]

    print("Deleting the following objects on S3:")
    print("\n".join([f" - {fname}" for fname in keys_in_s3_not_in_local]))
    print("Uploading the following objects to S3")
    print("\n".join([f" - {fname}" for fname in keys_in_local_not_in_s3]))

    if args.update:
        print("Updating the following objects on S3")
        print(
            "\n".join(
                [
                    f" - {fname} {local_mtime.isoformat()} > {s3_mtime.isoformat()}"
                    for fname, local_mtime, s3_mtime in keys_that_need_updating_on_s3
                ]
            )
        )
        print("Updating the following objects on Local")
        print(
            "\n".join(
                [
                    f" - {fname} {s3_mtime.isoformat()} > {local_mtime.isoformat()}"
                    for fname, s3_mtime, local_mtime in keys_that_need_updating_on_local
                ]
            )
        )

    if not args.dry_run:
        for key in keys_in_local_not_in_s3:
            upload_file(s3, args.pdfs, key, cfg["bucket_id"])

        if keys_in_s3_not_in_local:
            print("Deleting objects that should not be in S3 anymore")
            s3.delete_objects(
                Bucket=cfg["bucket_id"],
                Delete={"Objects": [{"Key": key} for key in keys_in_s3_not_in_local]},
            )

        if args.update:
            print("Updating objets on S3")
            for key, local_mtime, s3_mtime in keys_that_need_updating_on_s3:
                upload_file(s3, args.pdfs, key, cfg["bucket_id"])

            print("Downloading updated objects from S3 not supported yet")


if __name__ == "__main__":
    main()
