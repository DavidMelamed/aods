import { CopilotKit } from "@copilotkit/react";
import { useEffect, useState } from "react";

export default function Home() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/opportunities")
      .then((r) => r.json())
      .then(setItems)
      .catch((err) => console.error("fetch failed", err));
  }, []);

  return (
    <CopilotKit>
      <main style={{ padding: "2rem" }}>
        <h1>AODS Opportunities</h1>
        <table>
          <thead>
            <tr>
              <th>Keyword</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {items.map((op, i) => (
              <tr key={i}>
                <td>{op.keyword}</td>
                <td>{op.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </CopilotKit>
  );
}
