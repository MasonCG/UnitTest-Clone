import sys
import inspect
import importlib
import os

mod_name = 'coolTests'
mod = importlib.import_module(mod_name)

klasses = [k for k, obj in inspect.getmembers(mod) if inspect.isclass(obj)]

klass = getattr(sys.modules[mod_name], klasses[0])

methods = inspect.getmembers(klass, predicate=inspect.isfunction)
methods[:] = [m for name, m in methods]

meths = {}
for m in methods:
    mSigniture = inspect.signature(m)
    parameters = mSigniture.parameters
    for key, value in parameters.items():
        meths[m] = (key)

for key, value in meths.items():
    print(f'{key} -> [\n\t{value}\n]')

print(type(mod))


