let bookId = null;
const userId = "user-001"; // static for now

async function uploadPDF() {
  const fileInput = document.getElementById("pdfUpload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", file); // Change this line

  const res = await fetch("http://localhost:8000/books/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  bookId = data.book_id;

  document.getElementById(
    "response"
  ).innerText = `📄 Uploaded! Pages: ${data.num_pages}`;
}

async function askQuestion() {
  const question = document.getElementById("question").value;
  if (!bookId || !question) {
    alert("Upload a book and enter a question first.");
    return;
  }

  const res = await fetch("http://localhost:8000/query/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      book_id: bookId,
      question: question,
    }),
  });

  const data = await res.json();
  document.getElementById("response").innerText = `🤖 Answer:\n${data.answer}`;
}

async function getSummary() {
  if (!bookId) {
    alert("Upload a book first.");
    return;
  }

  const res = await fetch("http://localhost:8000/query/summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      book_id: bookId,
    }),
  });

  const data = await res.json();
  document.getElementById("response").innerText = `📚 Summary:\n${data.answer}`;
}
