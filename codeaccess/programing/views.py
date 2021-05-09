from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileEdit, UpdateProfileImg
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import CLanguage
from django.http import JsonResponse
import json
from .complier import *


# Create your views here.

@login_required
def profile(request):
    """Returning user profile .."""
    return render(request, 'programing/userprofile.html')


@login_required
def updateprofile(request):
    """Profile updateing .."""
    if request.method == "POST":
        form = ProfileEdit(request.POST, instance=request.user.profile)
        print(form.is_valid())
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            # messages.success(request,'Your Profile has been updated!')

            return redirect('programing:profile')

    form = ProfileEdit(instance=request.user.profile)
    return render(request, 'programing/profile-edit.html', {"form": form, 'title': 'profile-edit'})


@login_required
def updatepofileimg(request):
    """Updating profile image ...."""
    if request.method == 'POST':
        print("yess")
        form = UpdateProfileImg(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            print(form.is_valid())

            form.save()

            return redirect('programing:profile')
    form = UpdateProfileImg(instance=request.user.profile)
    return render(request, 'programing/profile-edit.html', {"form": form, 'title': 'profile-edit'})


@login_required
def post_detail(request, year, month, day, post):
    """Return post object detail..."""
    problem = get_object_or_404(CLanguage, slug=post, publish__year=year,
                                publish__month=month, publish__day=day)
    indata = problem.testcase
    outdata = problem.output
    problem.testcase = problem.testcase.split(';')

    problem.output = problem.output.split(';')

    testcase = zip(problem.testcase, problem.output)

    return render(request, 'programing/test-compiler.html', {'post': problem, 'testcase': testcase, 'indata': indata, 'outdata': outdata})


class CList(LoginRequiredMixin, ListView):
    """list c language problem ..."""

    queryset = CLanguage.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'programing/list.html'


def execute(request):
    """Executing your program.."""
    template_data = {}
    if request.method == 'POST':
        form = request.POST.copy()  # CodeExecutorForm(request.POST)

        if form:
            executor = Compiler()
            code = form.get('code')  # cleaned_data['code']
            input_data = form.get('input')  # cleaned_data['input']
            expected_output = form.get('output')  # cleaned_data['output']
            print(expected_output)
            if not expected_output:
                executor.set_custom_input(True)
            test_cases = genrate_testcase(input_data, expected_output)
            try:
                for test_case in test_cases:
                    executor.add_test_case(test_case)
            except:
                pass
            lan = Language(int(form.get('language')))

            if len(input_data) == 0 or input_data is None:
                template_data['error'] = "Invalid code"
                return render(request, 'generic_error.html', template_data)
            else:
                if lan == Language.C or lan == Language.CPP or lan == Language.JAVA or lan == Language.PYTHON:
                    executor.set_code(code)
                    executor.set_language(lan)

                    execution_result = executor.execute()
                    executor.delete_code_file()
                    print(execution_result.name)
                    template_data['result'] = execution_result.name
                    if execution_result.name == 'COE':
                        template_data['output'] = executor.error[0]
                        return JsonResponse(json.dumps(template_data), safe=False)

                    if executor.iscustominput:
                        template_data['output'] = executor.out_puts[0]

                        return JsonResponse(json.dumps(template_data), safe=False)

                    template_data['test_cases_total'] = executor.get_num_test_cases()
                    if executor.get_num_field_test_cases() is not None:
                        template_data['test_cases_passed'] = executor.get_num_test_cases() - executor.get_num_field_test_cases()

                    if executor.hasExecuted and not executor.iscustominput:
                        checked_values, expected_output = executor.compare_out_puts()
                        display_data = []
                        outputs = executor.get_output()
                        errors = executor.get_errors()
                        for i in range(len(outputs)):
                            if executor.hasError:
                                e = errors[i]
                            else:
                                e = None
                            temp_tuple = (i, checked_values[i], outputs[i], expected_output[i], e)
                            display_data.append(temp_tuple)
                        template_data['display_data'] = display_data

                    return JsonResponse(json.dumps(template_data), safe=False)  # render(request, 'OutputView.html', template_data)

    return HttpResponse("Cannot sanitize form data")
