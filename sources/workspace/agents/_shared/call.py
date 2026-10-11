#!/usr/bin/env python3
"""Call ArtCraft MCP tools from the shell. One server process per invocation, so calls share a session.
  call.py <app> --list                         # tool names + args
  call.py <app> <tool> '<json args>'           # one call
  call.py <app> --seq steps.json|-             # [[tool,{args}],...] in one session
Env CRAFT_WORKDIR sets photocraft's write root (relative paths go there)."""
import json,sys,os,subprocess,select,time
LAUNCH="/workspace/media-mcp/launch.sh"
def session(app):
    p=subprocess.Popen([LAUNCH,app],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    n=[0]
    def rpc(method,params=None,timeout=120):
        n[0]+=1; i=n[0]
        p.stdin.write(json.dumps({"jsonrpc":"2.0","id":i,"method":method,"params":params or {}})+"\n"); p.stdin.flush()
        end=time.time()+timeout
        while time.time()<end:
            if select.select([p.stdout],[],[],1)[0]:
                l=p.stdout.readline()
                if not l: break
                try: m=json.loads(l)
                except ValueError: continue
                if m.get("id")==i: return m
        return {"error":"timeout/no reply"}
    rpc("initialize",{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"call.py","version":"1"}})
    p.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"})+"\n"); p.stdin.flush()
    return p,rpc
def show(name,m):
    r=m.get("result")
    if r is None: print(f"## {name}: ERROR {json.dumps(m.get('error'))}"); return False
    out=[]
    for c in r.get("content",[]):
        out.append(c["text"] if c.get("type")=="text" else f"<{c.get('type')} {c.get('mimeType','')} {len(c.get('data',''))}b>")
    err=r.get("isError")
    print(f"## {name}: {'ERROR' if err else 'ok'}\n"+"\n".join(out)[:4000]); return not err
if __name__=="__main__":
    if len(sys.argv)<3: print(__doc__); sys.exit(2)
    app=sys.argv[1]; p,rpc=session(app); ok=True
    try:
        if sys.argv[2]=="--list":
            for t in rpc("tools/list")["result"]["tools"]:
                s=t.get("inputSchema",{}); req=set(s.get("required") or [])
                args=", ".join((a+"*" if a in req else a) for a in (s.get("properties") or {}))
                print(f"- {t['name']}({args})")
        elif sys.argv[2]=="--seq":
            src=sys.stdin if sys.argv[3]=="-" else open(sys.argv[3])
            for name,args in json.load(src):
                ok=show(name,rpc("tools/call",{"name":name,"arguments":args})) and ok
        else:
            a=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
            ok=show(sys.argv[2],rpc("tools/call",{"name":sys.argv[2],"arguments":a}))
    finally: p.kill()
    sys.exit(0 if ok else 1)
