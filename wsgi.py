def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/json')])
    return [b"[Hello]"]