import { Outlet } from "react-router";

export function Layout() {
  return (
    <div className="min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Repo Digest Tool
        </h1>
        <Outlet />
      </div>
    </div>
  );
}
