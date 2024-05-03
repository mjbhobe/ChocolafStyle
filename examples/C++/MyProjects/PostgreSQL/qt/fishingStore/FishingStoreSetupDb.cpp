#include "FishingStoreSetupDb.h"

#include <iostream>
#include <pqxx/pqxx>
#include <vector>
using namespace std;

// static
void FishingStoreSetupDb::createDbObjects(pqxx::connection& conn)
{
    dropTables(conn);
    createTables(conn);
}

void FishingStoreSetupDb::dropTables(pqxx::connection& conn)
{
    // drop all tables if they exist
    cout << "Dropping tables..." << endl;
    pqxx::work txn(conn);
    try {
        cout << "  - customers" << endl;
        txn.exec0("DROP TABLE IF EXISTS customers CASCADE");
        cout << "  - stores" << endl;
        txn.exec0("DROP TABLE IF EXISTS stores CASCADE");
        cout << "  - orders" << endl;
        txn.exec0("DROP TABLE IF EXISTS orders CASCADE");
        cout << "  - products" << endl;
        txn.exec0("DROP TABLE IF EXISTS products CASCADE");
        cout << "  - order_products" << endl;
        txn.exec0("DROP TABLE IF EXISTS order_products CASCADE");
        txn.commit();
    } catch (const pqxx::sql_error& err) {
        // cerr << "SQL Error: " << err.what() << endl;
        // cerr << "Query was: " << err.query() << endl;
        throw err;
    } catch (const std::exception& err) {
        // cerr << "Error: " << err.what() << endl;
        throw err;
    }
}

void FishingStoreSetupDb::createTables(pqxx::connection& conn)
{
    // create all tables
    pqxx::work txn(conn);

    try {
        cout << "Creating tables..." << endl;

        cout << "  - customers" << endl;
        txn.exec0(
            R"(
            CREATE TABLE customers(
                customer_id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(25),
                email VARCHAR(255) NOT NULL)
            )");

        cout << "  - stores" << endl;
        txn.exec0(
            R"(
            CREATE TABLE stores(
                store_id SERIAL PRIMARY KEY,
                store_name VARCHAR(100) not null,
                phone VARCHAR(25),
                state VARCHAR(5))
            )");

        cout << "  - orders" << endl;
        txn.exec0("CREATE TABLE orders("
                  "   order_id SERIAL PRIMARY KEY,"
                  "   customer_id INTEGER,"
                  "   order_date TEXT NOT NULL,"
                  "   order_status INTEGER NOT NULL,"
                  "   store_id INTEGER NOT NULL,"
                  "   FOREIGN KEY (customer_id) REFERENCES customers(customer_id),"
                  "   FOREIGN KEY (store_id) REFERENCES stores(store_id)"
                  ")");

        cout << "  - products" << endl;
        txn.exec0("CREATE TABLE products("
                  "   product_id SERIAL PRIMARY KEY,"
                  "   product_name VARCHAR(100) NOT NULL,"
                  "   model_year VARCHAR(100) NOT NULL,"
                  "   list_price DECIMAL(10, 2) NOT NULL"
                  ")");

        cout << "  - order_products" << endl;
        txn.exec0("CREATE TABLE order_products("
                  "   order_id INTEGER NOT NULL,"
                  "   product_id INTEGER NOT NULL,"
                  "   quantity INTEGER NOT NULL,"
                  "   list_price DECIMAL(10, 2) NOT NULL,"
                  "   FOREIGN KEY (order_id) REFERENCES orders(order_id),"
                  "   FOREIGN KEY (product_id) REFERENCES products(product_id)"
                  ")");

        txn.commit();
    } catch (const pqxx::sql_error& err) {
        // cerr << "SQL Error: " << err.what() << endl;
        // cerr << "Query was: " << err.query() << endl;
        throw err;
    } catch (const std::exception& err) {
        // cerr << "Error: " << err.what() << endl;
        throw err;
    }
}

// static
void FishingStoreSetupDb::populateDb(pqxx::connection& conn)
{
    cout << "Populating tables..." << endl;
    try {
        pqxx::work txn(conn);

        // customers table
        struct customer_data_rec {
            string first_name;
            string last_name;
            string phone;
            string email;
        };
        std::vector<customer_data_rec> customer_recs {
            { "James", "Smith", "", "NULL" },
            { "Mary", "Johnson", "", "NULL" },
            { "John", "Williams", "", "NULL" },
            { "Patricia", "Brown", "", "(716) 472-1234" },
            { "Lijing", "Ye", "", "NULL" },
            { "Andrea", "Cotman", "", "NULL" },
            { "Aaron", "Rountree", "", "NULL" },
            { "Malik", "Ranger", "", "NULL" },
            { "Helen", "Rodriguez", "", "NULL" },
            { "Linda", "Martinez", "", "NULL" },
            { "William", "Hernandez", "", "(757) 408-1121" },
            { "Elizabeth", "Lopez", "", "(804) 543-9876" },
            { "David", "Gonzalez", "", "NULL" },
            { "Barbara", "Wilson", "", "NULL" },
            { "Richard", "Anderson", "", "NULL" },
            { "Susan", "Thomas", "", "(213) 854-7771" },
            { "Joseph", "Taylor", "", "(609) 341-9801" },
            { "Jessica", "Moore", "", "(707) 121-0909" },
            { "Thomas", "Jackson", "", "NULL" },
            { "Sarah", "Martin", "", "NULL" },
            { "Ryan", "Lee", "", "NULL" },
            { "Cynthia", "Perez", "", "(754) 908-­5432" },
            { "Jacob", "Thompson", "", "(763) 765-1023" },
            { "Kathleen", "White", "", "NULL" },
            { "Gary", "Harris", "", "NULL" },
            { "Amy", "Sanchez", "", "(213) 198-4510" },
            { "Nicholas", "Clark", "", "NULL" },
            { "Shirley", "Ramirez", "", "(231) 480-1567" },
            { "Eric", "Lewis", "", "NULL" },
            { "Angela", "Miller", "", "NULL" }
        };

        conn.prepare("insert_customers",
            "INSERT INTO customers (first_name, last_name, email, phone)"
            "VALUES ($1, $2, $3, $4)");

        cout << "  - customers " << flush;
        size_t num_recs = 0;
        for (const auto& [first_name, last_name, email, phone] : customer_recs) {
            txn.exec_prepared(
                "insert_customers", first_name, last_name, email, phone);
            num_recs++;
        }
        cout << "(" << num_recs << " records inserted)" << endl;

        struct stores_data_rec {
            string store_name;
            string phone;
            string state;
        };

        std::vector<stores_data_rec> store_recs {
            { "Boston Fish Supplies", "(617) 987-6543", "MA" },
            { "Miami Fish Supplies", "(786) 123-4567", "FL" }
        };

        conn.prepare("insert_stores",
            "INSERT INTO stores (store_name, phone, state)"
            "VALUES ($1, $2, $3)");

        cout << "  - stores " << flush;
        num_recs = 0;
        for (const auto& [store_name, phone, state] : store_recs) {
            txn.exec_prepared("insert_stores", store_name, phone, state);
            num_recs++;
        }
        cout << "(" << num_recs << " records inserted)" << endl;

        txn.commit();
    } catch (const pqxx::sql_error& err) {
        // cerr << "SQL Error: " << err.what() << endl;
        // cerr << "Query was: " << err.query() << endl;
        throw err;
    } catch (const std::exception& err) {
        // cerr << "Error: " << err.what() << endl;
        throw err;
    }
}
