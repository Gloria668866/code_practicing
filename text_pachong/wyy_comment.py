# import requests
#
# # 用你抓包时的encSecKey
# encSecKey="6dbbec0b6ba856ea2f5034fe89715e1f4b5108d6d512bb7f6cda762cda7cee40cecb561a8930aedcbbc700d86338e42a23b81e0b58081cd4b45e76a84d6fce5d53e8319a126c8fff7109fc3270516f050332a2377aaaf0b425a0daf224443df284eaa0f121ca9de0ddf58b91e65298f6b9ec5381dc20772b3e137286e19c90ff"
#
# url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=5982076564c4c82226cee89ebaa9af36"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Referer": "https://music.163.com/album?id=274821019",
#     "Cookie": "_ga=GA1.1.1713397532.1743663210; Qs_lvt_382223=1743663210; Qs_pv_382223=684702676692165900; _clck=yack55%7C2%7Cfur%7C0%7C1919; _ga_C6TGHFPQ1H=GS1.1.1743663210.1.1.1743663221.0.0.0; NTES_P_UTID=j8HykQsGD4YqVXjyxxOIUA7ecu1XSHHr|1744592862; _iuqxldmzr_=32; _ntes_nnid=4041ba32c054e66a8ba733b9f45c44d0,1751433810139; _ntes_nuid=4041ba32c054e66a8ba733b9f45c44d0; NMTID=00O90EpRpvVXe0mc0btlV7eiZiK1hEAAAGXyZcRuA; WEVNSM=1.0.0; WNMCID=ahnvex.1751433812542.01.0; sDeviceId=YD-9%2BQBR2fgSF1EFwBUAUfTf7GXwm5G6Ary; ntes_utid=tid._.TTbgDOf7zy1FAhRRRVeGe%252BCXh24CrEu3._.0; WM_TID=u9L9FiDG1fhAVEFURALCO%2FWTgj4NyVlB; __snaker__id=06ETajxPwxT3I24R; ntes_kaola_ad=1; gdxidpyhxdE=rxuzrV3g%2BG9jN44HCXJCpvs7DmGlp2vRiU1%5Cz80ruhzQz2%5COeEkW1Rx%5CpzAui1QCizWMqgvmHOHzMH%2Fa1jczy0P2NpwSUJabaE59LmbWEN%2FnWdrjS7wjz1YypAEtfBK%5CPlNQGJ%5C%2BDvwLGIbuG8jt1PrDdkpYEOwjPxf9T0DAzns%2B4MrJ%3A1751450705133; __remember_me=true; P_INFO=18723978458|1751450029|1|music|00&99|null&null&null#jis&320100#10#0|&0|null|18723978458; MUSIC_U=001AE7456DA3B8B1A7A3934E7F418F595F886E60A4AADC2ED0C1158D5DCD5E8A049B47381A038196AAB65DEF6D9474709A0ED6C96F55F33684228A04ED5B73EFCCCA08BE93770742C3B2BD5DFCAE11B891ADBF6DA5D7ED7F7F27AD353EEB80E10CB9432A7F7201AF4ADF05308FCE7558DC1243D357FF74481F02825752A2BA2D2B9F0DF43A54975DFE0D6FCCFE920DF2EA9D905E88C5FF0CCD366C126E58C0BD6C1D5D2BB3BE7AB2A5C3A8A0F37AC2ECC677848D2EFA1F64CDBAEBF4AEFD8FA963FA62A6DE6E464D2AE610C0C82E6D387C30E860E59F5539AFEF5AC580F728AD44E03E3C6509CB630A312FC04BD1D2EDF90B0731A11C1D514B6313D22573CA09A31CC3E571CCA192E85FDD0C23A98C2DC095D9807CFD62D79659025CBB644AAC74C1857DE91DC94BBDFB7755446DE64A7BC9AC33CE8C4F35C80C44979BCC3272C292632BE6E6FCDC125AD4562BB22D75C66229834B7CF19DCDE6E660AA7FF231DD198777A95C858A2CE0BFA8A21D7B8C86; __csrf=5982076564c4c82226cee89ebaa9af36; JSESSIONID-WYYY=qU3yk69qwglv5gSWqk9Jiaob0e9P8AnMi5%2FpBFU%2BDtUuaRX7zprS2EGS7kZx0IAFfzmWaqMqYH8jSTXnxNJNEfpNSMdBwKHHYJ16GAnZexb6mhI8%2B0uyDTATEgNI%2FvUAMIJbvlRPOSt9Ch8RANX6Z49krPFMKJtl79zZpS9%5CO1OmKFc8%3A1751601112058; WM_NI=f8TfNSxN2BVsscaF34bbLpC8F2qC9fMBf47vvgCkNbQVcVNDqHq8TTVDGMPWcfcyQSRXDZIGdWiuN4DvRXzAHhK00W95%2FdwxvuG1ZHRhyBNP2geNq5VyAKdCIipiphDyRTc%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7b26298b589a6bb62b5928ab7c55b869e8eaddb6fb2bd8586ed5d87e7878cf72af0fea7c3b92aa6e89c87cd59bc92fea3d579b1bdafa7b240a2be8491c23486eebfa4bc6e8f9eaad5b67eb6b98d8ccd6a938aadb7cd50b398bfd9d760969c89aed35da1baad9ad45992888cbbcc4da889a796cd4088aa9eb9f94b8cb885d1b35dfbebe185f674b6ab89d2d94492b8b7a3cd5cf2b9abaff43f96a78face7498bb7c08af36488a79eb5e237e2a3"
# }
# post_data = {
#     "params": "seyadEnrbJspysgnQlICDlwWw0m1GVK6PdpnG5qHNN1DVg4ylcVg6NQOJ9hdq7A5xbYPebaBr5t4eNzUNBv2HSZXm5Qsp4EwNE6H6jBngSGSTNY8eZh4dn4c1X7W96qqR3WYDtYIx8pRC6IgnmZoTImEZGHnjvvcWwfzuLXtTHApyoGf1hKjIQFIAQ+gTdclMWvZZUQ0emVZ3+nPdxTYjd0d3MfqSAawl7Y+qKam0PWWf/Hqd0qAhXUZb4gAXmQHs8O8CrJI0ZXHTubt74r+XF5r7v8neZ3lhlQUiRe+AWIZPpvi9mqenE7AfPp4C+8/MwIkQuosblOaF+VYVpI5L6PpblpMjgt/+UjDHoDQC0A=",
#     "encSecKey": "3b1c9393e0e241cf5b9ffd28b7a2589b9174162daa22dcff25203743112c2ec8b7eda8fd1b8bcc06a91c2d3e2195944258fbcc5b6c8e4be1dae2e41c398553ddf178c04a158329f048849cd1a928a4f6b5865e640560185f3b311c71f6deeb59038cdb2761d809768e5129dc39a171b4b41e66462aa2b94950be5f6facd8992e"
# }
#
# resp = requests.post(url, data=post_data, headers=headers)
# print(resp.status_code)
#
# result = resp.json()
# for comment in result['data']['comments']:
#     print(comment['user']['nickname'], ":", comment['content'])
#
# with open('comments.txt', 'w', encoding='utf-8') as f:
#     for comment in result['data']['comments']:
#         f.write(f"{comment['user']['nickname']} : {comment['content']}\n")
#


#  ----           ---------------- 方法二
import base64
import json
import random
import string
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

def get_random_str(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def aes_encrypt(text, key, iv='0102030405060708'):
    text = pad(text.encode('utf-8'), AES.block_size)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encrypted = cipher.encrypt(text)
    return base64.b64encode(encrypted).decode('utf-8')

def rsa_encrypt(text, pubKey, modulus):
    text = text[::-1]  # 先反转
    rs = int(binascii.hexlify(text.encode()), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def get_params_and_encSecKey(data):
    pubKey = "010001"
    modulus = ("00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725"
               "152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312"
               "ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424"
               "d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8"
               "e7")
    nonce = "0CoJUm6Qyw8W8jud"
    iv = "0102030405060708"
    text = json.dumps(data)
    secKey = get_random_str(16)
    encText = aes_encrypt(aes_encrypt(text, nonce, iv), secKey, iv)
    encSecKey = rsa_encrypt(secKey, pubKey, modulus)
    return encText, encSecKey

# 请求参数
data = {
    "rid": "R_AL_3_274821019",
    "threadId": "R_AL_3_274821019",
    "pageNo": 1,
    "pageSize": 20,
    "cursor": "-1",
    "offset": "0",
    "orderType": 1
}

params, encSecKey = get_params_and_encSecKey(data)

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=5982076564c4c82226cee89ebaa9af36"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://music.163.com/album?id=274821019",
    "Cookie": "_ga=GA1.1.1713397532.1743663210; Qs_lvt_382223=1743663210; Qs_pv_382223=684702676692165900; _clck=yack55%7C2%7Cfur%7C0%7C1919; _ga_C6TGHFPQ1H=GS1.1.1743663210.1.1.1743663221.0.0.0; NTES_P_UTID=j8HykQsGD4YqVXjyxxOIUA7ecu1XSHHr|1744592862; _iuqxldmzr_=32; _ntes_nnid=4041ba32c054e66a8ba733b9f45c44d0,1751433810139; _ntes_nuid=4041ba32c054e66a8ba733b9f45c44d0; NMTID=00O90EpRpvVXe0mc0btlV7eiZiK1hEAAAGXyZcRuA; WEVNSM=1.0.0; WNMCID=ahnvex.1751433812542.01.0; sDeviceId=YD-9%2BQBR2fgSF1EFwBUAUfTf7GXwm5G6Ary; ntes_utid=tid._.TTbgDOf7zy1FAhRRRVeGe%252BCXh24CrEu3._.0; WM_TID=u9L9FiDG1fhAVEFURALCO%2FWTgj4NyVlB; __snaker__id=06ETajxPwxT3I24R; ntes_kaola_ad=1; gdxidpyhxdE=rxuzrV3g%2BG9jN44HCXJCpvs7DmGlp2vRiU1%5Cz80ruhzQz2%5COeEkW1Rx%5CpzAui1QCizWMqgvmHOHzMH%2Fa1jczy0P2NpwSUJabaE59LmbWEN%2FnWdrjS7wjz1YypAEtfBK%5CPlNQGJ%5C%2BDvwLGIbuG8jt1PrDdkpYEOwjPxf9T0DAzns%2B4MrJ%3A1751450705133; __remember_me=true; P_INFO=18723978458|1751450029|1|music|00&99|null&null&null#jis&320100#10#0|&0|null|18723978458; MUSIC_U=001AE7456DA3B8B1A7A3934E7F418F595F886E60A4AADC2ED0C1158D5DCD5E8A049B47381A038196AAB65DEF6D9474709A0ED6C96F55F33684228A04ED5B73EFCCCA08BE93770742C3B2BD5DFCAE11B891ADBF6DA5D7ED7F7F27AD353EEB80E10CB9432A7F7201AF4ADF05308FCE7558DC1243D357FF74481F02825752A2BA2D2B9F0DF43A54975DFE0D6FCCFE920DF2EA9D905E88C5FF0CCD366C126E58C0BD6C1D5D2BB3BE7AB2A5C3A8A0F37AC2ECC677848D2EFA1F64CDBAEBF4AEFD8FA963FA62A6DE6E464D2AE610C0C82E6D387C30E860E59F5539AFEF5AC580F728AD44E03E3C6509CB630A312FC04BD1D2EDF90B0731A11C1D514B6313D22573CA09A31CC3E571CCA192E85FDD0C23A98C2DC095D9807CFD62D79659025CBB644AAC74C1857DE91DC94BBDFB7755446DE64A7BC9AC33CE8C4F35C80C44979BCC3272C292632BE6E6FCDC125AD4562BB22D75C66229834B7CF19DCDE6E660AA7FF231DD198777A95C858A2CE0BFA8A21D7B8C86; __csrf=5982076564c4c82226cee89ebaa9af36; JSESSIONID-WYYY=qU3yk69qwglv5gSWqk9Jiaob0e9P8AnMi5%2FpBFU%2BDtUuaRX7zprS2EGS7kZx0IAFfzmWaqMqYH8jSTXnxNJNEfpNSMdBwKHHYJ16GAnZexb6mhI8%2B0uyDTATEgNI%2FvUAMIJbvlRPOSt9Ch8RANX6Z49krPFMKJtl79zZpS9%5CO1OmKFc8%3A1751601112058; WM_NI=f8TfNSxN2BVsscaF34bbLpC8F2qC9fMBf47vvgCkNbQVcVNDqHq8TTVDGMPWcfcyQSRXDZIGdWiuN4DvRXzAHhK00W95%2FdwxvuG1ZHRhyBNP2geNq5VyAKdCIipiphDyRTc%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7b26298b589a6bb62b5928ab7c55b869e8eaddb6fb2bd8586ed5d87e7878cf72af0fea7c3b92aa6e89c87cd59bc92fea3d579b1bdafa7b240a2be8491c23486eebfa4bc6e8f9eaad5b67eb6b98d8ccd6a938aadb7cd50b398bfd9d760969c89aed35da1baad9ad45992888cbbcc4da889a796cd4088aa9eb9f94b8cb885d1b35dfbebe185f674b6ab89d2d94492b8b7a3cd5cf2b9abaff43f96a78face7498bb7c08af36488a79eb5e237e2a3"
}

post_data = {
    "params": params,
    "encSecKey": encSecKey
}

resp = requests.post(url, data=post_data, headers=headers)

try:

    print(resp.status_code)
    result = resp.json()
    for comment in result['data']['hotComments']:
        print(comment['user']['nickname'], ":", comment['content'])
except Exception as e:
    print("请求或解析出错：", e)
    print("返回内容：", resp.text)






