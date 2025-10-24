import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <h1 className="text-4xl font-bold mb-6">UniVerse Test Page</h1>

      {/* Test Card */}
      <Card className="w-full max-w-sm mb-6">
        <CardHeader>
          <CardTitle>Test Card</CardTitle>
        </CardHeader>
        <CardContent>
          <p>This is a simple Shadcn Card component.</p>
        </CardContent>
      </Card>

      {/* Test Button */}
      <Button variant="default">Click Me</Button>
    </div>
  );
}

export default App;
