import math, time
class Telemetry:
    def __init__(self):
        self.calls=0; self.prompt_chars=0; self.response_chars=0; self.tool_calls=0; self.started=time.time()
    def model_call(self,messages,response):
        self.calls+=1
        self.prompt_chars += sum(len(m.get('content','')) for m in messages)
        self.response_chars += len(response or '')
    def tool_call(self): self.tool_calls+=1
    def snapshot(self):
        local_tokens=math.ceil((self.prompt_chars+self.response_chars)/4)
        return {
          'model_calls':self.calls,'tool_calls':self.tool_calls,
          'estimated_local_tokens':local_tokens,
          'estimated_cloud_tokens_avoided':local_tokens,
          'prompt_chars':self.prompt_chars,'response_chars':self.response_chars,
          'elapsed_seconds':round(time.time()-self.started,2)
        }
