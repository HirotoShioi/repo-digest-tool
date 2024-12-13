import { BrowserRouter, Routes, Route } from "react-router";
import RepositoriesPage from "./pages/Repositories";
import RepositoryDetailsPage from "./pages/RepositoryDetails";
import { Layout } from "./components/Layout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<RepositoriesPage />} />
          <Route path="/:author/:name" element={<RepositoryDetailsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
