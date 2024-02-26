"""
Module keys.py
"""
import logging

import boto3
import botocore.exceptions

import src.elements.service as sr


class Keys:
    """
    Class Keys

    Notes
    -----

    Gets lists of Amazon S3 keys.
    """

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of an Amazon S3 bucket in focus.
        """

        self.__bucket_name = bucket_name
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__s3_client = service.s3_client
        self.__bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger: logging.Logger = logging.getLogger(__name__)

    def particular(self, prefix: str) -> list[str]:
        """

        :param prefix: Amazon S3 (Simple Storage Service) prefix.
        :return:
            A list of Amazon S3 (Simple Storage Service) keys.
        """

        try:
            dictionaries = self.__s3_client.list_objects_v2(Bucket=self.__bucket_name, Prefix=prefix)
        except self.__s3_client.exceptions.NoSuchKey as err:
            raise Exception(err) from err
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

        items = [dictionary['Key'] for dictionary in dictionaries['Contents']]

        return items

    def all(self) -> list[str]:
        """

        :return:
            A list of Amazon S3 (Simple Storage Service) keys.
        """

        try:
            state: dict = self.__bucket.meta.client.head_bucket(Bucket=self.__bucket.name)
        except self.__bucket.meta.client.exceptions.NoSuchBucket as err:
            raise Exception(err) from err
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

        if state:
            items = [k.key for k in list(self.__bucket.objects.all())]
        else:
            items = []

        return items
