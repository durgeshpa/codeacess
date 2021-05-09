"""compiler logic..."""
from enum import Enum
import subprocess
import random
import os


class Language(Enum):
    """defining type of language ClassName.."""

    C = 1
    CPP = 2
    JAVA = 3
    PYTHON = 4


class ExecutionStatus(Enum):
    """exucuation Enum class will return exution status.."""

    NYR = 0  # Still executing may take some more time to get result
    ACC = 1  # executed sucessfully with correct solution
    WRA = 2  # executed sucessfully with wrong solution
    TLE = 3  # excuted but time timit exceed
    COE = 4  # complition error field
    RTE = 5  # error during run time
    INE = 6  # internal error has been promoted


class TestCase:
    """sotring all the test caes ..."""

    input_data = None
    output_data = None

    def __init__(self, input_data, expected_output):
        """Storing input and expected output for test case.."""
        self.input_data = input_data
        self.output_data = expected_output

    def get_input(self):
        """Return input data .."""
        return self.input_data

    def get_output(self):
        """Return expected output.."""
        return self.output_data


def genrate_testcase(input_string, output_string):
    """Genrate no of test cases on the basis of output and input .."""
    test_case = []
    inputs = [x.strip() for x in input_string.split(sep=';')]
    outputs = [x.strip() for x in output_string.split(sep=';')]

    if len(inputs) is not len(outputs):  # input test case and out put test case not same..
        return None

    else:
        # remove blank space due to split function
        if len(inputs[len(inputs) - 1]) == 0:
            del inputs[len(inputs) - 1]
            del outputs[len(outputs) - 1]

        for i in range(len(inputs)):
            test_case.append(TestCase(inputs[i], outputs[i]))

        return test_case


def genrate_random_name(length):
    """Genrae random name for file .."""
    file_name = ''
    for i in range(length):
        base = 97 if random.randint(0, 1) == 0 else 65
        offset = random.randint(0, 25)
        file_name += chr(base + offset)

    return file_name


class Compiler:
    """compiler envornment setting .."""

    exc_status = None  # it denote that progam has not not been executed yet
    code = None
    template = None
    test_cases = None
    out_puts = None
    error = None
    failed_test_cases = None
    language = None
    filename = None
    hasError = False
    hasExecuted = False
    hasFile = False
    maxExecTime = 5  # affter five second program will auto matically terminate
    iscustominput = False

    def add_test_case(self, test_case):
        """Adding test case.."""
        if isinstance(test_case, TestCase):
            if self.test_cases is None:
                self.test_cases = []
            self.test_cases.append(test_case)

        else:
            raise ValueError("Trying invalid TestCase")

        return

    def get_num_test_cases(self):
        """Return total no of test cases.."""
        if self.test_cases is None:
            return 0

        else:
            return len(self.test_cases)

    def get_num_field_test_cases(self):
        """Retun total no of faild test cases.."""
        return self.failed_test_cases

    def set_language(self, l):
        """Seting languge for compile or run..."""
        if isinstance(l, Language):
            self.language = l

        else:
            self.language = None
            raise ValueError("Invalid language")

    def set_code(self, code):
        """Set the code.."""
        self.code = code

    def set_template(self, template=None):
        """Setting template .."""
        if template is not None:
            self.template = template + "\r\n"

        return

    def set_max_exc_time(self, time=5):
        """Set maximum time for executaion ..."""
        self.maxExecTime = time

    def get_output(self):
        """Return out pt if program executed ..."""
        if self.hasExecuted:
            return self.out_puts

        else:
            return None

    def get_errors(self):
        """Return list of error according to the respective test cases.."""
        if self.hasError:
            return self.error

        else:
            return None

    def contain_erros(self):
        """Program during comile time has error or not.."""
        return self.hasError

    def genrate_code_file(self, lang):
        """Create file for running the coding .."""
        self.filename = genrate_random_name(10)
        if self.filename is None:
            print("error")

        if self.template is not None:
            complete_code = self.template + "\r\n"

        else:
            complete_code = self.code + "\r\n"

        if lang == 'java':
            with open('Main.java', "w") as f:
                f.write('package ' + self.filename + ';\n')
                f.write(complete_code)
                f.flush()
                f.close()

        else:
            self.filename = self.filename + '.' + str(lang)
            with open(self.filename, "w") as f:
                # f.write('package\t' + self.filename.split('.')[0].strip() + ';')
                f.write(complete_code)
                f.flush()
                f.close()

    def delete_code_file(self):
        """Delete code file .."""
        if self.filename is None:
            print("file not exist")

        try:
            os.remove(self.filename)
            os.remove(self.filename.split('.')[0])

        except:
            try:
                import shutil
                os.remove('Main.java')
                shutil.rmtree(self.filename)

            except:
                pass

        self.hasFile = False
        self.filename = None

    def compare_out_puts(self):
        """Comparing program output put and expected out put..."""
        index = 0
        values = []
        expect = []

        for test_case in self.test_cases:
            expected_output = test_case.get_output()
            # print(self.out_puts,"rakesh")
            # print(len(self.test_cases))
            expected_output = expected_output.replace(chr(13), '')
            actual_output = self.out_puts[index].strip()
            actual_output = actual_output.replace(chr(13), '')
            # print(actual_output)
            # print(expected_output)
            # print(len(actual_output))
            # print((len(expected_output)))
            values.append(expected_output == actual_output)
            # print(index)
            expect.append(expected_output)
            index = index + 1
        return values, expect

    def set_custom_input(self, bools=False):
        """Set input custom .."""
        self.iscustominput = bools

    def execute(self):
        """Execution of program.."""
        self.exec_status = ExecutionStatus.NYR

        if self.language is not None:
            if self.language == Language.C or self.language == Language.CPP or self.language == Language.JAVA or self.language == Language.PYTHON:
                if self.language == Language.C:
                    self.genrate_code_file(lang='c')
                    commond = ['gcc', self.filename, '-o', self.filename.split('.')[0]]

                elif self.language == Language.CPP:
                    self.genrate_code_file(lang='cpp')
                    commond = ['g++', '-std=c++11', self.filename, '-o', self.filename.split('.')[0]]

                elif self.language == Language.JAVA:
                    self.genrate_code_file(lang='java')
                    commond = ['javac', '-d', '.', 'Main.java']

                elif self.language == Language.PYTHON:
                    self.genrate_code_file(lang='py')

                    # print(commond)
                if self.out_puts is None:
                    self.out_puts = []
                if self.error is None:
                    self.error = []
                # commond = ['gcc', self.filename, '-o', self.filename.split('.')[0]]
                error = None
                if self.language != Language.PYTHON:
                    process = subprocess.Popen(commond, stderr=subprocess.PIPE)
                    error = process.communicate()
                    error = error[1].decode("utf-8")
                    process.kill()
                    print(error)

                if error is None or 'error' not in error:
                    if self.language == Language.JAVA:
                        commond = 'java\t' + self.filename + ".Main"

                    elif self.language == Language.PYTHON:
                        commond = 'python\t' + self.filename

                    else:
                        commond = './{}'.format(self.filename.split('.')[0])

                    self.hasExecuted = True
                    for test_case in range(len(self.test_cases)):
                        process = subprocess.Popen([commond], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                        try:
                            out, error = process.communicate(bytes(self.test_cases[test_case].get_input(), "ascii"), timeout=self.maxExecTime)
                            self.out_puts.append(out.decode('utf-8'))
                            process.kill()
                            # print(error)

                            if len(error) != 0:
                                self.error.append(error.decode('utf-8'))
                                self.hasError = True

                            else:
                                self.error.append(None)
                                process.kill()

                        except subprocess.TimeoutExpired:
                            if process is not None:
                                process.kill()
                            self.hasExecuted = False
                            self.exec_status = ExecutionStatus.TLE
                            break

                    if self.hasExecuted and not self.iscustominput:
                        comparisons, expect = self.compare_out_puts()
                        if False in comparisons:
                            self.exec_status = ExecutionStatus.WRA
                            self.failed_test_cases = comparisons.count(False)

                        else:
                            self.exec_status = ExecutionStatus.WRA
                            self.failed_test_cases = 0

                else:
                    self.exec_status = ExecutionStatus.COE
                    self.error.append(error)

            else:
                print("another programing language")
                self.exec_status = ExecutionStatus.INE

        else:
            print("no programing langage is selected")
            self.exec_status = ExecutionStatus.INE

        return self.exec_status
