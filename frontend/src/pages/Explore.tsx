import Classes from "@/components/Classes";
import ClassGroups from "@/components/ClassGroups";
import CreateClassModal from "@/components/CreateClassModal";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export default function Explore() {
    const [modalOpen, setModalOpen] = useState(false);
    const { user } = useAuth();

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
                <div className="flex items-center justify-center mb-2 relative">
                    <h1 className="text-4xl font-bold">Explore Classes</h1>
                    <Button
                        disabled={!user}
                        onClick={() => setModalOpen(true)}
                        className="absolute right-0"
                    >
                        + Create Class
                    </Button>
                </div>
                <p className="text-primary/70 mb-8 text-center">
                    Browse all available classes and join discussions.
                </p>
            </div>
            {/* Classes Grid */}
            <div className="w-full">
                <Classes />
            </div>
            
            <CreateClassModal
                open={modalOpen}
                onOpenChange={setModalOpen}
                onSuccess={() => {
                    // Refresh classes list or navigate
                    window.location.reload();
                }}
            />
        </div>
    );
}