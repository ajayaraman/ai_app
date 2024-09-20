from fasthtml.common import *
import sqlite3

# Add Tailwind CSS and custom styles
tailwind_cdn = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
custom_styles = Style("""
    body { @apply bg-gray-100 text-gray-800; }
    th { @apply bg-blue-100 text-left p-3 font-semibold; }
    td { @apply p-3; }
    tr:nth-child(even) { @apply bg-gray-50; }
    tr:nth-child(odd) { @apply bg-white; }
    tr:hover { @apply bg-gray-200; }
    .container { @apply max-w-6xl; }
    #usersTable { @apply rounded-lg overflow-hidden shadow-lg; }
    #searchInput { @apply bg-white border-gray-300 focus:ring-blue-500 focus:border-blue-500; }
    .status-badge { @apply px-2 inline-flex text-xs leading-5 font-semibold rounded-full; }
    .status-online { @apply bg-green-100 text-green-800; }
    .status-away { @apply bg-yellow-100 text-yellow-800; }
    .status-not-available { @apply bg-red-100 text-red-800; }
    .modal { @apply fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full; }
    .modal-content { @apply relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white; }
""")
app, rt = fast_app(hdrs=(tailwind_cdn, custom_styles))

def status_badge(status):
    status_class = {
        'Online': 'bg-green-100 text-green-800',
        'Away': 'bg-yellow-100 text-yellow-800',
        'Not Available': 'bg-red-100 text-red-800'
    }.get(status, 'bg-gray-100 text-gray-800')
    return Div(status, cls=f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status_class}")

@rt('/show_form')
def add_user_form():
    return Div(
        Div(
            H2("Add New User", cls="text-xl mb-4"),
            Form(
                Input(type="text", name="name", placeholder="Name", cls="w-full p-2 mb-2 border rounded"),
                Input(type="email", name="email", placeholder="Email", cls="w-full p-2 mb-2 border rounded"),
                Select(
                    Option("Online", value="Online"),
                    Option("Away", value="Away"),
                    Option("Not Available", value="Not Available"),
                    name="status",
                    cls="w-full p-2 mb-2 border rounded"
                ),
                Button("Add User", type="submit", cls="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"),
                cls="space-y-4",
                hx_post="/add_user",
                hx_target="#usersTable tbody",
                hx_swap="beforeend",
                hx_on="htmx:afterRequest: this.reset()"
            ),
            Button("Close", cls="mt-4 bg-gray-300 hover:bg-gray-400 text-black font-bold py-2 px-4 rounded",
                   hx_get="/close_modal",
                   hx_target="#modal",
                   hx_swap="outerHTML"),
            cls="modal-content"
        ),
        id="modal",
        cls="modal"
    )

@rt('/close_modal')
def close_modal():
    return Div(id="modal")

@rt('/')
def get():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()    
    # Fetch all users from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Create the table HTML
    table = Table(
        Thead(Tr(Th("ID"), Th("Name"), Th("Email"), Th("Status"))),
        Tbody(
            *(Tr(
                Td(user['id']),
                Td(user['name']),
                Td(user['email']),
                Td(status_badge(user['status']))
            ) for user in users)
        ),
        id="usersTable",
        cls="w-full border-collapse"
    )

    # Create the search input
    search_input = Input(type="text", id="searchInput", placeholder="Search by name or email", 
                         cls="mb-4 p-2 border rounded w-full",
                         hx_trigger="keyup changed delay:500ms",
                         hx_get="/search",
                         hx_target="#usersTable tbody")

    # Add button to show the form
    add_button = Button("Add User", 
                        cls="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mb-4",
                        hx_get="/show_form",
                        hx_target="#modal",
                        hx_swap="innerHTML")

    return Titled("User Database",
                  Div(H1("User Database", cls="text-3xl font-bold mb-4 text-gray-800"),
                      add_button,
                      Div(id="modal"),
                      search_input, 
                      table, 
                      cls="container mx-auto p-4"))

@rt('/add_user')
def post(name: str, email: str, status: str):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Insert the new user into the database
    cursor.execute("INSERT INTO users (name, email, status) VALUES (?, ?, ?)", (name, email, status))
    conn.commit()
    
    # Get the ID of the newly inserted user
    new_user_id = cursor.lastrowid
    
    # Close the database connection
    conn.close()
    
    # Return the new row to be added to the table
    return Tr(
        Td(new_user_id),
        Td(name),
        Td(email),
        Td(status_badge(status))
    )

@rt('/search')
def search(searchInput: str):
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE name LIKE ? OR email LIKE ?", 
                   (f'%{searchInput}%', f'%{searchInput}%'))
    users = cursor.fetchall()
    
    conn.close()
    
    return Tbody(
        *(Tr(
            Td(user['id']),
            Td(user['name']),
            Td(user['email']),
            Td(status_badge(user['status']))
        ) for user in users)
    )

serve()