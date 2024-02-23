"""
Module objects.py
"""
import logging

import boto3
import botocore.exceptions

import src.elements.service as sr


class Objects:
    """
    Class Objects
    """

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of the Amazon S3 (Simple Storage Service) bucket in focus
        """

        self.__bucket_name: str = bucket_name
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__s3_client = service.s3_client
        self.__bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger: logging.Logger = logging.getLogger(__name__)

    def filter(self, prefix: str):
        """
        This function creates "... an iterable of all ObjectSummary resources in the collection filtered by ... " <prefix>

        :param prefix: The folder
        :return:
            An iterable
        """

        try:
            return self.__bucket.objects.filter(Prefix=prefix)
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

    def all(self):
        """
        "Creates an iterable of all ObjectSummary resources in the collection."

        :return:
            An iterable
        """

        try:
            return self.__bucket.objects.all()
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err
