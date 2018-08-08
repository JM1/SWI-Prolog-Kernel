import os
import os.path as op
import tempfile
import IPython
import jupyter_client
from IPython.utils.process import getoutput

def exec_swipl(code):
    source_path, target_path = setup_env()

    with open(source_path, 'w') as f:
        f.write(code)

    os.system("swipl {0:s} > {1:s}".format(source_path, target_path))  # source_path, program_path))
    #out = os.system("swipl {0:s} ".format(source_path))  # source_path, program_path))
    f = open(target_path, 'r')
    return f.read()

def setup_env():
    dirpath = '/home/max/.local/share/jupyter/kernels/swi/temp'  # tempfile.mkdtemp()

    source_path = op.join(dirpath, 'temp.pl')
    target_path = op.join(dirpath, 'out.txt')
    return source_path, target_path


    

"""SWI-Prolog kernel wrapper"""
from ipykernel.kernelbase import Kernel

class SwiplKernel(Kernel):

    # Khttp://localhost:8890/notebooks/swipl_testing.ipynb#ernel information.
    implementation = 'SWI-Prolog'
    implementation_version = '0.0'
    language = 'Prolog'
    language_version = '1.0'
    language_info = {'name': 'swipl',
                     'mimetype': 'text/plain'}
    banner = "SWI-Prolog Kernel"

    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):
        """This function is called when a code cell is
        executed."""
        if not silent:
            # We run the Prolog code and get the output.
            output = exec_swipl(code)

            # We send back the result to the frontend.
            stream_content = {'name': 'stdout',
                              'text': output}
            self.send_response(self.iopub_socket,
                              'stream', stream_content)
        return {'status': 'ok',
                # The base class increments the execution
                # count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SwiplKernel)
