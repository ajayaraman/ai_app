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
""")
app, rt = fast_app(hdrs=(tailwind_cdn, custom_styles))

def status_badge(status):
    status_class = {
        'Online': 'bg-green-100 text-green-800',
        'Away': 'bg-yellow-100 text-yellow-800',
        'Not Available': 'bg-red-100 text-red-800'
    }.get(status, 'bg-gray-100 text-gray-800')
    return Div(status, cls=f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status_class}")

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
                         cls="mb-4 p-2 border rounded w-full")

    # Add JavaScript for search functionality
    search_script = Script("""
        document.getElementById('searchInput').addEventListener('input', function() {
            var input, filter, table, tr, tdName, tdEmail, i, txtValueName, txtValueEmail;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("usersTable");
            tr = table.getElementsByTagName("tr");
            for (i = 1; i < tr.length; i++) {  // Start from 1 to skip header
                tdName = tr[i].getElementsByTagName("td")[1];  // Name column
                tdEmail = tr[i].getElementsByTagName("td")[2];  // Email column
                if (tdName && tdEmail) {
                    txtValueName = tdName.textContent || tdName.innerText;
                    txtValueEmail = tdEmail.textContent || tdEmail.innerText;
                    if (txtValueName.toUpperCase().indexOf(filter) > -1 || txtValueEmail.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        });
    """)

    return Titled("User Database",
                  Div(H1("User Database", cls="text-3xl font-bold mb-4 text-gray-800"),
                      search_input, 
                      table, 
                      cls="container mx-auto p-4"),
                  search_script)

serve()