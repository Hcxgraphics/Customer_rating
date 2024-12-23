import random
import string
import pandas as pd


class Customer:
    def __init__(self, customer_id, name, age, mobile_no, ratings):
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.mobile_no = mobile_no
        self.ratings = ratings

    def avg_rating(self):
        return sum(self.ratings) / len(self.ratings)

    @staticmethod
    def generate_cust(num_cust=100):
        cust = []
        for _ in range(num_cust):
            customer_id = random.randint(100, 999)
            name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8)))
            age = random.randint(18, 90)
            mobile_no = f"0{random.randint(1000000000, 9999999999)}"
            ratings = [round(random.uniform(1, 5), 2) for _ in range(random.randint(1, 10))]
            cust.append((customer_id, name, age, mobile_no, ratings))
        return cust

    @staticmethod
    def save_to_csv(cust, filename="customer_data.csv"):
        df = pd.DataFrame([{
            "Customer ID": customer[0],
            "Name": customer[1],
            "Age": customer[2],
            "Mobile No.": customer[3],
            "Ratings": customer[4]
        } for customer in cust])
        df.to_csv(filename, index=False)

    @staticmethod
    def load_csv(filename="customer_data.csv"):
        df = pd.read_csv(filename)
        df["Ratings"] = df["Ratings"].apply(eval)
        return df

    @staticmethod
    def rate_customers(df, threshold=3.5):
        customer_list = []
        for _, row in df.iterrows():
            cust = Customer(
                customer_id=row["Customer ID"],
                name=row["Name"],
                age=row["Age"],
                mobile_no=row["Mobile No."],
                ratings=row["Ratings"]
            )
            if cust.avg_rating() >= threshold:
                customer_list.append(cust)
        return customer_list


if __name__ == "__main__":
    random_customers = Customer.generate_cust()
    Customer.save_to_csv(random_customers)
    customer_df = Customer.load_csv()
    high_rated_customers = Customer.rate_customers(customer_df)
    table_data = [{
        "Name": customer.name,
        "Cust-ID": customer.customer_id,
        "Age": customer.age,
        "Contact": customer.mobile_no,
        "Avg-Rating": round(customer.avg_rating(), 2)
    } for customer in high_rated_customers]
    result = pd.DataFrame(table_data)

    print("Customers having average rating >= 3.5 :")
    print(result)
