import Classes from "@/components/Classes";
import ClassGroups from "@/components/ClassGroups";
import CreateClassModal from "@/components/CreateClassModal";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export default function Explore() {
    const [modalOpen, setModalOpen] = useState(false);
    const { user } = useAuth();
    const [query, setQuery] = useState("");

    return (
        <div className="flex flex-col items-center w-full max-w-7xl mx-auto mt-10 px-4">
            {/* Hero/Header (styled like Home) */}
            <div className="w-full mb-6">
                <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#234E70] via-[#1f6b8a] to-[#0ea5a4] text-white shadow-2xl p-6 sm:p-10">
                    <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center gap-6">
                        <div className="flex-1 text-center sm:text-left">
                            <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">Cross-Campus Classes</h1>
                            <p className="mt-2 text-sm sm:text-lg text-white/90">Browse and discuss topics from universities around the world.</p>
                        </div>

                        <div className="flex flex-col w-full sm:w-auto">
                            <p className="mt-2 text-l text-white/90 pb-2">Dont see a relevant cross-campus class?</p>

                            <Button
                                disabled={!user}
                                onClick={() => setModalOpen(true)}
                                className="ml-3 hover:cursor-pointer"
                            >
                                + Create Class
                            </Button>


                        </div>
                    </div>

                    {/* decorative accent */}
                    <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-3xl pointer-events-none" />

                    {/* small connector pill to visually attach the blurb card */}
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 w-28 h-6 bg-white/10 rounded-full pointer-events-none" />
                </div>
            </div>

            {/* CSE Blurb — visually connected (overlapping) */}
            <div className="w-full -mt-8 mb-6">
                <div className="max-w-4xl mx-auto relative z-10">
                    <Card className="shadow-lg ring-1 ring-black/5">
                        <CardContent>
                            <p className="mt-1 text-sm text-muted-foreground">
                                Our Class-Signature-Engine automatically detects when classes from different universities are essentially the same subject and groups them together without any manual input. Explore these groups to connect with peers from universities Australia-wide!
                            </p>
                        </CardContent>
                    </Card>
                </div>
            </div>

            {/* Class Groups list */}
            <div className="w-full">
                <ClassGroups />
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