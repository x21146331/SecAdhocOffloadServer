import subprocess
import time


class JavaExecutor(object):

    def startExecuting(self, classname, javafile, resourcename, params):
        compres = self.compile_java(javafile)
        print(compres)

        if compres.find("error") == -1 or compres.find("Exception") == -1:  # if build was successful start executing it
            execres = self.execute_java(classname, resourcename, params)
            if execres[2] is None:
                print("Finished running {} with params: {} in {} seconds".format(classname, params, execres[1]))
                return execres
        else:
            return None

    def compile_java(self, java_file):
        p = subprocess.Popen("cd java_classes && javac {}".format(java_file),
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()

        return output[0].decode("utf-8")

    def execute_java(self, classname, resourcename, params):
        tic = time.time()
        args = []
        if resourcename is not None:
            args.append(resourcename)
        if type(params) is int:
            args.append(params)
        else:
            args.append(" ".join(map(str, params)))

        cmd = "cd java_classes && java {} {}".format(classname, " ".join(args))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()

        duration = time.time() - tic

        return output, duration, errors
