import tkinter as tk
from tkinter import scrolledtext
import traceback
import sys
import io


error_explanations = {
    "SyntaxError": "Usually caused by missing colons, parentheses, or incorrect indentation.",
    "NameError": "Variable or function used before being defined. Check for typos or missing definitions.",
    "IndentationError": "Python requires consistent indentation. Ensure proper use of tabs or spaces.",
    "ZeroDivisionError": "Division by zero is not allowed. Add a condition to prevent it.",
    "TypeError": "Operation or function applied to the wrong data type. Verify your variable types.",
    "ValueError": "Correct data type but inappropriate value passed.",
    "AttributeError": "Trying to access an attribute that doesn't exist on the object.",
    "IndexError": "Index is out of range. Possibly accessing beyond list/tuple length.",
    "KeyError": "Trying to access a dictionary key that doesn’t exist.",
    "ModuleNotFoundError": "Trying to import a module that doesn't exist or isn't installed.",
    "ImportError": "Failed to import a module or a part of it.",
    "RecursionError": "Recursion went too deep. Check your base condition.",
}

def smart_fixer(error_type, line, code_lines):
    suggestions = []
    line_num = int(line) - 1
    if line_num >= len(code_lines):
        return ["# Line number out of range for suggestions."]
    original = code_lines[line_num].strip()

    if "SyntaxError" in error_type:
        if ":" not in original and any(k in original for k in ["if", "for", "while", "def", "elif", "else"]):
            suggestions.append(original + ":  # Added missing colon")
        if original.count("(") != original.count(")"):
            suggestions.append(original + ")  # Check for unmatched parentheses")
    elif "NameError" in error_type:
        suggestions.append("# Fix: Ensure the variable/function is defined before use.")
    elif "IndentationError" in error_type:
        suggestions.append("    " + original + "  # Properly indented line")
    elif "ZeroDivisionError" in error_type:
        suggestions.append(original.replace("/ 0", "/ 1") + "  # Avoid division by zero")
    elif "TypeError" in error_type:
        suggestions.append("# Fix: Check the data types passed to functions or operations.")
    elif "ValueError" in error_type:
        suggestions.append("# Fix: Ensure the value fits the expected range/type.")
    elif "AttributeError" in error_type:
        suggestions.append("# Fix: Verify that the object supports this attribute/method.")
    elif "IndexError" in error_type:
        suggestions.append("# Fix: Check that your index is within the range of the list/tuple.")
    elif "KeyError" in error_type:
        suggestions.append("# Fix: Use .get() or check if key exists in dictionary before accessing.")
    elif "ModuleNotFoundError" in error_type:
        suggestions.append("# Fix: Ensure the module is installed using pip.")
    elif "ImportError" in error_type:
        suggestions.append("# Fix: Check if you're importing correctly.")
    elif "RecursionError" in error_type:
        suggestions.append("# Fix: Add a base case to end recursion properly.")
    else:
        suggestions.append("# General error. Review your logic and syntax.")

    return suggestions

def debug_code(user_code):
    code_lines = user_code.strip().split('\n')
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    try:
        exec(user_code, {})
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
        return f"✅ BUG FREE\n\nOutput:\n{result}"
    except Exception as e:
        sys.stdout = sys.__stdout__
        tb = traceback.extract_tb(e.__traceback__)
        last = tb[-1]
        error_type = type(e).__name__
        line_num = last.lineno
        message = str(e)
        suggestions = smart_fixer(error_type, line_num, code_lines)
        explanation = error_explanations.get(error_type, "This is an uncommon error. Investigate the logic carefully.")

        suggestion_text = "\n".join(f"> {s}" for s in suggestions)
        report = f"""
❌ BUGGY CODE DETECTED

🛠️ Error Type: {error_type}
📌 Line Number: {line_num}

📝 Original Line:
> {code_lines[line_num - 1].strip() if line_num <= len(code_lines) else '[Unavailable]'}

💡 AI Suggestions:
{suggestion_text}

🧠 Explanation:
{explanation}

🚫 Error Message:
{message}
"""
        return report, line_num

def run_debugger():
    user_code = code_input.get("1.0", tk.END)
    result = debug_code(user_code)

    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)

    if isinstance(result, tuple):
        report, error_line = result
        result_box.insert(tk.END, report)
        try:
            start = f"{error_line + 12}.0"
            end = f"{error_line + 12}.end"
            result_box.tag_config("highlight", background="#ff3cac", foreground="white")
            result_box.tag_add("highlight", start, end)
        except:
            pass
    else:
        result_box.insert(tk.END, result)

    result_box.config(state='disabled')

root = tk.Tk()
root.title("💡 AI Python Debugger")
root.geometry("1000x750")
root.config(bg="#0f0f0f")

title = tk.Label(root, text="💡 AI Python Debugger", fg="#00f7ff", bg="#0f0f0f", font=("Consolas", 22, "bold"))
title.pack(pady=10)

code_input = scrolledtext.ScrolledText(root, height=15, width=110, bg="#1e1e1e", fg="#00ff90", insertbackground="white", font=("Courier", 12))
code_input.pack(pady=10)

run_button = tk.Button(root, text="🔍 Run AI Debugger", command=run_debugger, bg="#00f7ff", fg="#0f0f0f", font=("Consolas", 14, "bold"))
run_button.pack(pady=10)

result_box = scrolledtext.ScrolledText(root, height=20, width=110, bg="#111111", fg="#ff3cac", font=("Courier", 12))
result_box.pack(pady=10)
result_box.config(state='disabled')

root.mainloop()
