import { Hero } from "@/components/dashboard/Hero";
import { UploadCard } from "@/components/dashboard/UploadCard";
import { RecentWorkspaceList } from "@/components/dashboard/RecentWorkspaceList";

export default function DashboardPage() {
  return (
    <div className="flex flex-col space-y-12 pb-10">
      <Hero />
      
      <div className="mx-auto w-full max-w-3xl">
        <UploadCard />
      </div>

      <div className="pt-8">
        <RecentWorkspaceList />
      </div>
    </div>
  );
}
