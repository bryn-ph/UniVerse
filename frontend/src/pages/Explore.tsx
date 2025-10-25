import Classes from "@/components/Classes";
import ClassGroups from "@/components/ClassGroups";

export default function Explore() {
    return (
        <div className="flex flex-col items-center w-full max-w-7xl mx-auto mt-10 px-4">
            {/* Header */}
            <div className="w-full">
                <h1 className="text-4xl font-bold mb-2 text-center">Explore Class Groups</h1>
                <p className="text-primary/70 mb-8 text-center">
                    Browse all available class groups and join discussions.
                </p>
            </div>

            <div className="w-full">
                <ClassGroups />
            </div>

            <div className="w-full">
                <h1 className="text-4xl font-bold mb-2 text-center">Explore Classes</h1>
                <p className="text-primary/70 mb-8 text-center">
                    Browse all available classes and join discussions.
                </p>
            </div>
            {/* Classes Grid */}
            <div className="w-full">
                <Classes />
            </div>
        </div>
    );
}