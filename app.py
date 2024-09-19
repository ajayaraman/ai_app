from fasthtml.common import *
import sqlite3

app, rt = fast_app()

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
        Thead(Tr(Th("ID"), Th("Name"), Th("Email"))),
        Tbody(
            *(Tr(Td(user['id']), Td(user['name']), Td(user['email'])) for user in users)
        ),
        id="usersTable",
        cls="w-full border-collapse"
    )

    # Create the search input
    search_input = Input(type="text", id="searchInput", placeholder="Search by name or email", 
                         cls="mb-4 p-2 border rounded w-full bg-gray-800 text-white")

    # Add Tailwind CSS and custom styles
    tailwind_cdn = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
    custom_styles = Style("""
        body { @apply bg-gray-900 text-white; }
        th { @apply bg-gray-800 text-left p-2; }
        td { @apply border-t border-gray-700 p-2; }
        tr:hover { @apply bg-gray-700; }
        .container { @apply max-w-4xl; }
    """)

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
                  tailwind_cdn,
                  custom_styles,
                  Div(H1("User Database", cls="text-2xl font-bold mb-4"),
                      search_input, 
                      table, 
                      cls="container mx-auto p-4"),
                  search_script)

serve()