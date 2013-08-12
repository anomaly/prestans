#!/usr/bin/env python
import os
import sys

def main():

    import prestans.devel.gen

    #preplate = prestans.devel.gen.Preplate(template_type="closure.model", model_file="../demo/app/pdemo/rest/models.py", namespace="pdemo.data.model", output_directory="")
    preplate = prestans.devel.gen.Preplate(template_type="closure.filter", model_file="../demo/app/pdemo/rest/models.py", namespace="pdemo.data.filter", output_directory="")

    return preplate.run()

if __name__ == "__main__":

    prestans_path = os.path.join("..", "..")

    #:
    #: While in development attempt to import prestans from top dir
    #:
    if os.path.isdir(prestans_path):
    
        sys.path.insert(0, prestans_path)
        try:
            import prestans.devel
        except:
            del sys.path[0]

    else:
        import prestans.devel

    sys.exit(main())