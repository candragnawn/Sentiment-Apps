'use client'
import { useState } from "react"
import { Button } from "@/src/app/dashboard/components/ui/button"
import { Field } from "@/src/app/dashboard/components/ui/field"
import { Input } from "@/src/app/dashboard/components/ui/input"

export function InputInline() {
    const [keyword, setKeyword] = useState("")
    const [loading, setLoading] = useState(false)
  return (
    <Field orientation="horizontal">
      <Input type="search" placeholder="Search..." />
      <Button>Search</Button>
    </Field>
  )
}
