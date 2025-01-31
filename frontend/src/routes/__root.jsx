import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { useTranslationStore } from "@/store/useTranslation";
import {
    IconTable,
    IconChartSankey,
    IconTableAlias,
  } from "@tabler/icons-react";

export const Route = createRootRoute({
  component: () => {
    const { translate } = useTranslationStore();

    return (
        
      <>
      {/* 🛠 */}
        <div className="p-2 flex justify-center items-center gap-4 w-full">
          <div className="flex space-x-4 border-b border-gray-300 w-full justify-center">
            <Link
              to="/table"
              className="text-gray-600 hover:text-green-300 py-2 px-4 text-sm font-medium [&.active]:font-bold [&.active]:border-b-2 [&.active]:border-green-300"
            >
              <IconTable className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
              <span>{translate("Table")}</span>
            </Link>
            <Link
              to="/charts"
              className="text-gray-600 hover:text-green-300 py-2 px-4 text-sm font-medium [&.active]:font-bold [&.active]:border-b-2 [&.active]:border-green-300"
            >
             <IconChartSankey className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
             <span>{translate("Charts")}</span>
            </Link>
            <Link
              to="/ptable"
              className="text-gray-600 hover:text-green-300 py-2 px-4 text-sm font-medium [&.active]:font-bold [&.active]:border-b-2 [&.active]:border-green-300"
            >
             <IconTableAlias className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
             <span>{translate("Table P")}</span>
            </Link>
          </div>
        </div>

        <hr className="my-4" />

        <Outlet />

      </>
    );
  },
});
