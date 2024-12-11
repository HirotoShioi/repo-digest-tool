import { BrowserRouter, Routes, Route } from "react-router";
import { RepositoriesPage } from "./pages/RepositoriesPage";
import { RepositoryDetailsPage } from "./pages/RepositoryDetailsPage";
import { Layout } from "./components/Layout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<RepositoriesPage />} />
          <Route path="repository/:id" element={<RepositoryDetailsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
