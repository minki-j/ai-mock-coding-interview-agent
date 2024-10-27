from fasthtml.common import *

from app.utils.code_interpreter import execute_code

async def run_python(request):
    form_data = await request.form()
    code = form_data.get("code")

    result = execute_code(code)
    return P(result)
