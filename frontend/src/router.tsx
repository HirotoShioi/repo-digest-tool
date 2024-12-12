import { BrowserRouter, Routes, Route } from "react-router";
import RepositoriesPage from "./pages/Repositories";
import RepositoryDetailsPage from "./pages/RepositoryDetails";
import { Layout } from "./components/Layout";
import SettingsPage from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<RepositoriesPage />} />
          <Route
            path="repository/:author/:name"
            element={<RepositoryDetailsPage />}
          />
          <Route
            path="/repository/:author/:name/settings"
            element={<SettingsPage />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
