#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by bu on 2017-05-10
"""
from __future__ import unicode_literals
import json as complex_json
import requests
from utils import verify_sign
from utils import get_sign


class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }

    def __init__(self, api_key, secret_key, headers=dict()):
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = self.__headers
        self.headers.update(headers)

    def set_authorization(self, params):
        params['api_key'] = self.api_key
        self.headers['api_key'] = self.api_key
        self.headers['AUTHORIZATION'] = get_sign(params, self.secret_key)

    def request(self, method, url, params=dict(), data='', json=dict()):
        method = method.upper()
        if method == 'GET':
            self.set_authorization(params)
            result = requests.request('GET', url, params=params, headers=self.headers)
        else:
            if data:
                json.update(complex_json.loads(data))
            self.set_authorization(json)
            result = requests.request(method, url, json=json, headers=self.headers)
        return result


class OAuthClient(object):
    def __init__(self, request):
        self.request = request
        self._body = dict()
        self._authorization = ''

    @property
    def body(self):
        raise NotImplementedError('extract body')

    @property
    def authorization(self):
        raise NotImplementedError('authorization')

    def verify_request(self, secret_key):
        return verify_sign(self.body, secret_key, self.authorization)


class FlaskOAuthClient(OAuthClient):
    @property
    def body(self):
        if self._body:
            return self._body

        if self.request.method == 'GET':
            self._body = self.request.args.to_dict()
        elif self.request.is_json:
            self._body = self.request.json

        api_key = self.request.headers.get('API_KEY')
        if api_key:
            self._body['api_key'] = api_key
        return self._body

    @property
    def authorization(self):
        if self._authorization:
            return self._authorization

        self._authorization = self.request.headers['AUTHORIZATION']
        return self.authorization

