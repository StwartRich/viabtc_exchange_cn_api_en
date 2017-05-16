#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by bu on 2017-05-16
"""
from __future__ import unicode_literals
from python.oauth import RequestClient


def get_account():
    request_client = RequestClient(
            api_key='7DA46FDC6137469AA66F7D29020EB588',
            secret_key='9E4141D8EE9D4C6E9A65BA827441CCB2D05B921CD809A57A'
    )
    result = request_client.request('GET', 'https://www.viabtc.cn/api/v1/balance/')
    return result


if __name__ == '__main__':
    get_account()
