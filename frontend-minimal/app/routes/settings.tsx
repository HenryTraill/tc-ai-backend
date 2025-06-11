import type { Route } from "./+types/settings";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "TutorCruncher AI - Settings" },
    { name: "description", content: "App settings and preferences" },
  ];
}

export default function Settings() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

      <div className="bg-white rounded-lg p-6 border border-black text-center">
        <p className="text-gray-500 text-lg">Coming Soon</p>
        <p className="text-gray-400 mt-2">App settings and preferences will be available here.</p>
      </div>
    </div>
  );
}