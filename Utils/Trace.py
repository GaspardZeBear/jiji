import logging

tracer=logging.getLogger("Trace")
sh=logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s <@Trace> - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
tracer.addHandler(sh)
tracer.setLevel(logging.INFO)
tracer.debug("Trace customized " + str(tracer))

def Trace(f) :
  tracer.debug("deco "+ f.__name__)
  def wrapper(*args,**kwargs) :
    a=list(args)
    tracer.debug( f.__name__ + '(' + ','.join(str(a)) +')')
    return(f(*args))
  return(wrapper)

