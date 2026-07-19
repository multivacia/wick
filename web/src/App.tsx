import {
  SCAFFOLD_NOTICE,
  SCAFFOLD_STATUS,
  SCAFFOLD_TITLE,
} from "./scaffoldCopy";

export function App() {
  return (
    <main className="scaffold" aria-labelledby="scaffold-title">
      <h1 id="scaffold-title">{SCAFFOLD_TITLE}</h1>
      <p>{SCAFFOLD_STATUS}</p>
      <p>{SCAFFOLD_NOTICE}</p>
    </main>
  );
}
