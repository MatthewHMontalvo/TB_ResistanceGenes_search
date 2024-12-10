document.addEventListener("DOMContentLoaded", () => {
    const geneNameInput = document.getElementById("gene_name");
    const suggestionsList = document.getElementById("suggestions");

    // Fetch suggestions from the server as the user types
    geneNameInput.addEventListener("input", async () => {
        const query = geneNameInput.value.trim();
        if (query.length === 0) {
            suggestionsList.innerHTML = ""; // Clear suggestions if input is empty
            return;
        }

        try {
            // Fetch autocomplete suggestions from the server
            const response = await fetch(`/mmontal4/practical_project/PYfinalprojectTB.py?autocomplete=1&query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error("Failed to fetch suggestions");
            }

            const suggestions = await response.json(); // Expecting a JSON array
            suggestionsList.innerHTML = ""; // Clear existing suggestions

            // Populate suggestions
            suggestions.forEach((suggestion) => {
                const listItem = document.createElement("li");
                listItem.textContent = suggestion;
                listItem.addEventListener("click", () => {
                    geneNameInput.value = suggestion; // Set clicked suggestion as input value
                    suggestionsList.innerHTML = ""; // Clear suggestions
                });
                suggestionsList.appendChild(listItem);
            });
        } catch (error) {
            console.error("Error fetching suggestions:", error);
            suggestionsList.innerHTML = ""; // Clear suggestions on error
        }
    });

    // Hide suggestions list when clicking outside the input field
    document.addEventListener("click", (event) => {
        if (!geneNameInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.innerHTML = ""; // Clear suggestions
        }
    });
});
