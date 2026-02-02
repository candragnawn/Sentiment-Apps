"use client";
import { useState } from "react";
import { Button } from "@/src/app/dashboard/components/ui/button";
import { Field } from "@/src/app/dashboard/components/ui/field";
import { Input } from "@/src/app/dashboard/components/ui/input";

export function InputInline() {
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/analyze?keyword=${encodeURIComponent(keyword)}`,
      );
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("gagal memulai analisis", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Field orientation="horizontal">
        <Input className="p-4"
          type="search"
          placeholder="Search Keyword..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)} className="bg-black border-zinc-700 text-white"
        />
        <Button onClick={handleSearch} disabled={loading}>{loading ? "Processing..." : "Search"}</Button>
      </Field>
    
  );
}
