import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import App from './App'

describe('Campaign dashboard', () => {
  it('renders the Salesforce dashboard sections and key values', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { name: /salesforce campaign performance/i }),
    ).toBeInTheDocument()
    expect(screen.getByText('$1.84M')).toBeInTheDocument()
    expect(screen.getByText('Campaign type success')).toBeInTheDocument()
    expect(screen.getByText('Activity mix')).toBeInTheDocument()
    expect(screen.getByText('Campaign type rollup')).toBeInTheDocument()
    expect(screen.getByText('Top campaigns')).toBeInTheDocument()
    expect(screen.getByText('Method notes')).toBeInTheDocument()
    expect(screen.getByText('Dreamforce ABM acceleration')).toBeInTheDocument()
  })
})
