from flask_restful import abort


def abort_if_limit_or_offset_is_bad(args):
    if not 'limit'in args or not args['limit'].isdigit() or int(args['limit'])<=0:
        abort(400, message="Wrong limit argument")
    elif not 'offset'in args or not args['offset'].isdigit() or int(args['offset'])<0:
        abort(400, message="Wrong offset argument")


def abort_if_etag_doesnt_match(etag, res_etag):
    if etag is None:
        abort(428, message="ETag is needed")
    if  res_etag != etag.replace('"',''):
        abort(412, message="ETag doesn't match")