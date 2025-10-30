from product_model import Product
from termcolor import colored


def delete_database_products():
    try:
        # Delete all existing documents in the collection
        delete_result = Product.collection.delete_many({})  # Deletes all documents in the collection
        print(colored(f"Deleted {delete_result.deleted_count} documents from the product collection.", 'cyan'))

        # Verify if the collection is empty
        remaining_count = Product.collection.count_documents({})
        if remaining_count == 0:
            return colored("All documents successfully deleted.", 'cyan')
        else:
            return colored(f"Some documents still remain in the collection: {remaining_count} left.", 'red')
    except Exception as e:
        print(f"An error occurred while deleting documents: {e}")



print(delete_database_products())
