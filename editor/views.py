from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import scripts.littleChecker as checker
import os


def index(request):
    return render(request, 'editor/home.html')


def createFile(text, extension, name="default"):
    # Creates a file in editor/tmp directory
    os.chdir('.')
    pwd = os.getcwd()
    print 'Current directory: ', pwd
    os.chdir('editor/scripts/')
    file_name = '%s.%s' % (name, extension)
    with open(file_name, 'w') as f:
        f.write(text)
    os.chdir(pwd)
    return file_name


@csrf_exempt
def execute(request):
    """Create a file on server code.language
        compile it using the script provided
        and return the result
    """
    if request.is_ajax():
        code = request.POST.get('sourceCode', '')
        lang = request.POST.get('sourceLang', '')
        inp = request.POST.get('sourceInp', '')
        name = request.POST.get('sourceName', '')
        print ('Received: Code: %s \n lang: %s \n inp: %s \n name: %s\n ' %
               (code, lang, inp, name))
        output = ""
        try:
            created = createFile(code, lang, name)
            print 'Created file %s successfully' % (created)
            output = checker.main(created, inp)
        except Exception, e:
            print str(e)
            output = "\nError creating file\n"
        finally:
            print (output)
            return HttpResponse(output)