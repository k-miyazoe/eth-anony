#defaultだとtokenしか返さないものを以下を追加することで、token以外も返すように変更する
def jwt_response_payload_handler(token, user=None, request=None):
    """ JWT認証のカスタムレスポンス
    """
    return {
        'token': token,
        'user_id': user.id,
        'user_key': user.user_key,
        'user_name':user.user_name,
        'user_eth_address': user.user_eth_address,
        'user_group': user.user_group,
        'user_point': user.user_point,
    }