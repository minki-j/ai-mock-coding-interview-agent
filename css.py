from fasthtml.common import *

main_css ="""
.main-page-loader{
    display:none;
}
.htmx-request.main-page-loader{
    display:inline;
    transform: translate(-50%, -50%);
    animation: pulse 2s ease-in-out infinite !important;
}
.btn-loader {
    position: relative;
    pointer-events: auto;
    opacity: 1;
}
.htmx-request.btn-loader {
    color: transparent;
    pointer-events: none;
}
.htmx-request.btn-loader::after {
    content: "Loading...";
    position: absolute;
    width: auto;
    height: auto;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #000000;
    font-size: 14px;
    animation: pulse 2s ease-in-out infinite !important;
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.2; }
    100% { opacity: 1; }
}
.error-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.error-modal .error-content {
    padding: 20px;
    border-radius: 5px;
    width: 80%;
    height: 80%;
    overflow: auto;
    position: relative;
    background-color: var(--pico-background-color);
    border: var(--pico-primary-border);
}
.error-modal .error-content .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    cursor: pointer;
    border: none;
}
.profile-section {
    text-align: right;
}

.question-container {
    margin-bottom: 25px;
    background-color: var(--card-background-color);
    padding: 15px;
    border-radius: 8px;
}

.question-text {
    font-weight: bold;
    margin-bottom: 10px;
}

.radio-group {
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
}

.radio-group label {
    display: flex;
    align-items: center;
    margin-right: 10px;
    margin-bottom: 5px;
    cursor: pointer;
}

.radio-group input[type="radio"] {
    margin-right: 5px;
}

.radio-label {
    font-size: 14px;
}

.btn-submit {
    background-color: var(--primary);
    color: var(--primary-inverse);
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-submit:hover {
    background-color: var(--primary-hover);
}

.response-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    table-layout: fixed;
}

.response-table th, .response-table td {
    text-align: center;
    vertical-align: middle;
    padding: 5px;
    border: 1px solid var(--table-border-color);
    font-size: 0.75rem;
}

.response-table td:first-child {
    text-align: center;
}

.response-table th:nth-child(2) { background-color: var(--color-1); }
.response-table th:nth-child(3) { background-color: var(--color-2); }
.response-table th:nth-child(4) { background-color: var(--color-3); }
.response-table th:nth-child(5) { background-color: var(--color-4); }
.response-table th:nth-child(6) { background-color: var(--color-5); }

@media (prefers-color-scheme: dark) {
    .response-table th:nth-child(2) { background-color: var(--color-1-dark); }
    .response-table th:nth-child(3) { background-color: var(--color-2-dark); }
    .response-table th:nth-child(4) { background-color: var(--color-3-dark); }
    .response-table th:nth-child(5) { background-color: var(--color-4-dark); }
    .response-table th:nth-child(6) { background-color: var(--color-5-dark); }
    .question-container {
        background-color: var(--card-background-color-dark);
    }
}

:root {
    --color-1: #ffcccb;
    --color-2: #ffdab9;
    --color-3: #fffacd;
    --color-4: #e0ffb1;
    --color-5: #b3e0ff;
    --color-1-dark: #664e4e;
    --color-2-dark: #665952;
    --color-3-dark: #66655c;
    --color-4-dark: #5c664a;
    --color-5-dark: #4a5966;
    --primary: #007bff;
    --primary-inverse: #fff;
    --primary-hover: #0056b3;
    --table-border-color: #ddd;
    --card-background-color: #f5f5f5;
    --card-background-color-dark: #333333;
}
"""
