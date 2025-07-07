
import os

#小说的具体内容的url  %22 其实就是双引号
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}



import requests
import asyncio
import time
import aiohttp
import aiofiles  #异步的文件读写模块
import json


async def downLoad(cid, b_id, title):
    data1 = {
        "book_id": b_id,
        "cid": f"{b_id}|{cid}",
        "need_bookinfo": 1}
    data = json.dumps(data1)

    # 进行异步操作
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://dushu.baidu.com/api/pc/getChapterContent?data={data}",
                               headers=headers) as resp:
            dic = await resp.json()
            file_path = os.path.join("novel", f"{title}.txt")
            # 确保novel文件夹存在
            os.makedirs("novel", exist_ok=True)
            # 直接用原始title作为文件名保存
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(dic['data']['novel']['content'])



async  def getCateLog(url):
    res = requests.get(url, headers=headers)
    dic = res.json()
    tasks=[]
    for item in dic['data']['novel']['items']:  # item就是对应每个章节的内容 名称和cid
        title = item['title']
        cid = item['cid']
        # 准备异步任务
        tasks.append(downLoad(cid,b_id,title))
    await asyncio.gather(*tasks)


headers={
"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Connection": "keep-alive",
"Content-Type": "application/x-www-form-urlencoded",
"Cookie": "BAIDUID=E9C7C2FBFF2CA9927CC04336200BA26F:FG=1; BAIDUID_BFESS=E9C7C2FBFF2CA9927CC04336200BA26F:FG=1; BAIDU_WISE_UID=wapp_1740404501041_2; ZFY=lYgEnX4SfzNGGsAlSEPpn8K1H8KL07K6kwzXF52h3qo:C; BIDUPSID=E9C7C2FBFF2CA9927CC04336200BA26F; PSTM=1747181808; BDUSS=VVvQmlPOWU0LUtnTFlyLU5DTUJwME5tYUhrajduSElTZk1STFJETGF5SUFwM3hvSVFBQUFBJCQAAAAAAQAAAAEAAACJDaIgyMjH6bXEuf65~rn-x~IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaVWgAGlVoR; BDUSS_BFESS=VVvQmlPOWU0LUtnTFlyLU5DTUJwME5tYUhrajduSElTZk1STFJETGF5SUFwM3hvSVFBQUFBJCQAAAAAAQAAAAEAAACJDaIgyMjH6bXEuf65~rn-x~IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaVWgAGlVoR; H_PS_PSSID=62325_62832_63142_63325_63403_63514_63567_63564_63583_63578_63638_63628_63275_63646_63653_63725_63726_63706; H_WISE_SIDS=62325_62832_63142_63325_63403_63514_63567_63564_63583_63578_63638_63628_63275_63646_63653_63725_63726_63706; H_WISE_SIDS_BFESS=62325_62832_63142_63325_63403_63514_63567_63564_63583_63578_63638_63628_63275_63646_63653_63725_63726_63706; Hm_lvt_bf1e478a71b02a743ab42bcfed9d1ff1=1751893502; HMACCOUNT=AC116E3A14187D89; Hm_lpvt_bf1e478a71b02a743ab42bcfed9d1ff1=1751893681",

"Referer":"https://dushu.baidu.com/pc/reader?gid=4306063500&cid=1569782244",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
}

if __name__ == '__main__':
    b_id = '4306063500'
    url = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":'+ b_id +'}'  # 所有章节的内容（名称，cid）
    asyncio.run(getCateLog(url))



