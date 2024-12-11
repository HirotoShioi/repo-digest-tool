import { Outlet } from "react-router";

export function Layout() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Repository Management
        </h1>
        <Outlet />
      </div>
    </div>
  );
}
