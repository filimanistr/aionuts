# -*- coding: utf-8 -*-
import random
import aiohttp
import traceback
from .utils.utils import *
from .utils.colors import *
from asyncio import CancelledError

main_funcs=['call', 'send', 'lp_loop_gen']
class vkmain:
    def __init__(self, token, id, is_group = False):
        self.token = token
        self.is_grp = is_group
        self.id = id

    async def get_session(self):
        return aiohttp.ClientSession()

    async def call(self, method, d={}, **args):
        param = {'v':'5.131','access_token':self.token}
        param.update(d)
        param.update(args)
        url = 'https://api.vk.com/method/'+method
        async with self.session.post(url, data=param) as ret:
            resp = await ret.json()

        if 'error' in resp.keys():
            raise Exception('VkError: '+str(resp['error']))
        return D(resp)

    async def send(self, snd, text, attach=None):
        ln=len(text)
        if ln > 4096:
            for i in range(int(ln/4096)+1):
                await self.call('messages.send',peer_id=snd,message=text[i*4096:(i+1)*4096],random_id=random.randint(0,2**10))
            return True
        else: return await self.call('messages.send',peer_id=snd,message=text,attachment=attach,random_id=random.randint(0,2**10))

    async def GetLP(self):
        try:
            if self.is_grp:
                response = await self.call('groups.getLongPollServer',lp_version=3,group_id=self.id)
                return response.response
            response = await self.call('messages.getLongPollServer',lp_version=3)
            return response.response
        except Exception:
            print_c(RED+'longpoll error: ')
            traceback.print_exc()
            return await self.GetLP()

    async def lp_loop_gen(self):
        self.session = await self.get_session()
        self.lp = await self.GetLP()
        if self.is_grp:
            t = '{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3'
        else:
            t = 'http://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3'
        while True:
            try:
                sv = t.format(self.lp.server, self.lp.key, self.lp.ts)
                async with self.session.get(sv) as ret:
                    resp = await ret.json()

                response = D(resp)
                if response:
                    self.lp.ts=response.ts
                    for result in response.updates:
                        yield result
            except Exception:
                print_c(RED+'error:')
                traceback.print_exc()
                self.lp = await self.GetLP( )
            except CancelledError:
                print('shutting down')
                await self.session.close()
                break


class Bot:
    class _submethod:
        def __init__(self, vk , name):
            self._name = name
            self._vk = vk
        def __getattr__(self,name):
            async def call(d = {},**args):
                d.update(args)
                return await self._vk.call(self._name+'.'+name, d)
            return call
    def __init__(self, token, id=0, is_group = False):
        self._vk=vkmain( token, id, is_group )
        self.is_group = is_group
    def __getattr__(self, name):
        if name in main_funcs:
            return getattr( self._vk, name)
        return self._submethod(self._vk, name)
