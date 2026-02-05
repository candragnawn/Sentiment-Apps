"use client";
import { useState } from "react";
import { Button } from "@/src/components/ui/button";
import { Field } from "@/src/components/ui/field";
import { Input } from "@/src/components/ui/input";
interface InputInlineProps {
  onStart?: () => void;
  onComplete: () => void;
}

export function InputInline({ onStart, onComplete }: InputInlineProps) {
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keyword) return;
    await fetch(`http://127.0.0.1:8000/analyze?keyword=${keyword}`);

    setLoading(true);
    onStart?.();
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/analyze?keyword=${encodeURIComponent(keyword)}`,
      );
      if (response.ok) {
        setTimeout(() => {
          setLoading(false);
          onComplete();
        }, 8000);
      } else {
        setLoading(false);
        onComplete();
      }
    } catch (error) {
      console.error("gagal memulai analisis", error);
      setLoading(false);
      onComplete();
    }
  };
  return (
    <Field orientation="horizontal">
      <Input
        type="search"
        placeholder="Search Keyword..."
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        className="bg-transparent border border-border px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-ring min-w-[300px]"
      />
      <Button onClick={handleSearch} disabled={loading} className="cursor-pointer">
        {loading ? "Processing..." : "Search"}
      </Button>
    </Field>
  );
}
