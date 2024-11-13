document.getElementById("transaction-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const type = document.getElementById("type").value;
    const category = document.getElementById("category").value;

    console.log("Start")
    console.log(amount)
    console.log(type)
    console.log(category)

    fetch("/add_transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"amount":amount, "type":type, "category":category, "user_id": 1 })  // Adjust user_id as needed
    })
    .then(response => response.json())
    .then(data => {
        console.log("Transaction added:", data);
        // Update summary and recent transactions
        let totalIncome = 0;
        let totalExpenses = 0;
        let totalNet = 0
        fetch("/transactions/type/income").then(response => response.json()).then(data => {
            console.log("All Income transactions", data);

            data.forEach(transaction => {
                totalIncome += parseFloat(transaction.amount);  
            });

            document.getElementById("total-income").textContent = `Income: $${totalIncome.toFixed(2)}`;

            fetch("/transactions/type/expense").then(response => response.json()).then(data => {
                console.log("All Expense transactions", data);
    
                data.forEach(transaction => {
                    totalExpenses += parseFloat(transaction.amount);  
                });
    
                document.getElementById("total-expense").textContent = `Expense: $${totalExpenses.toFixed(2)}`;
                totalNet = totalIncome - totalExpenses
                console.log("All Expense transactions", data);
                document.getElementById("net-value").textContent = `Net: $${totalNet.toFixed(2)}`;
            });
        });
    })
    .catch(error => console.error("Error:", error));
});
