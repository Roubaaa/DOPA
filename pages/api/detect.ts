import type { NextApiRequest, NextApiResponse } from 'next'
import formidable, { Fields, Files } from 'formidable'
import fs from 'fs'
import FormData from 'form-data'
import fetch from 'node-fetch'

// Get Python backend URL from environment variable
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:5000/api/detect'

export const config = {
  api: {
    bodyParser: false,
  },
}

// Function to check if Python backend is running
async function checkBackendConnection() {
  try {
    console.log('Checking Python backend connection...')
    const response = await fetch(PYTHON_BACKEND_URL, {
      method: 'OPTIONS',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.ok
  } catch (error) {
    console.error('Python backend connection check failed:', error)
    return false
  }
}

// Function to retry failed requests
async function fetchWithRetry(url: string, options: any, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      console.log(`Attempting to connect to Python backend (attempt ${i + 1}/${retries})...`)
      const response = await fetch(url, options)
      if (response.ok) {
        return response
      }
      console.error(`Backend returned status ${response.status}`)
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error)
      if (i === retries - 1) throw error
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
  throw new Error(`Failed after ${retries} attempts`)
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', 'true')
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  )

  if (req.method === 'OPTIONS') {
    res.status(200).end()
    return
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  // Check if Python backend is running
  const isBackendRunning = await checkBackendConnection()
  if (!isBackendRunning) {
    console.error('Python backend is not running')
    return res.status(503).json({
      error: 'Python backend is not running',
      details: 'Please start the Python backend server'
    })
  }

  console.log('Processing image upload request...')
  
  const form = formidable({
    keepExtensions: true,
    maxFileSize: 10 * 1024 * 1024, // 10MB max
  })

  try {
    const [fields, files] = await new Promise<[Fields, Files]>((resolve, reject) => {
      form.parse(req, (err, fields, files) => {
        if (err) reject(err)
        resolve([fields, files])
      })
    })

    console.log('Parsed form data')
    
    const fileArray = files.image
    if (!fileArray || fileArray.length === 0) {
      console.error('No image file provided')
      return res.status(400).json({ error: 'No image file provided' })
    }

    const file = fileArray[0]
    console.log(`Processing file: ${file.originalFilename}`)

    // Create form data
    const formData = new FormData()
    formData.append('image', fs.createReadStream(file.filepath), {
      filename: file.originalFilename || 'image.jpg',
      contentType: file.mimetype || 'image/jpeg'
    })

    try {
      console.log('Sending request to Python backend...')
      const response = await fetchWithRetry(PYTHON_BACKEND_URL, {
        method: 'POST',
        body: formData,
        headers: formData.getHeaders()
      })

      console.log('Python backend response status:', response.status)
      const data = await response.json()
      console.log('Successfully processed image')

      // Clean up temp file
      fs.unlink(file.filepath, (err) => {
        if (err) console.error('Error cleaning up temp file:', err)
        else console.log('Cleaned up temp file:', file.filepath)
      })

      return res.status(200).json(data)
    } catch (error) {
      console.error('Error communicating with Python backend:', error)
      return res.status(503).json({
        error: 'Failed to communicate with Python backend',
        details: error instanceof Error ? error.message : 'Unknown error'
      })
    }
  } catch (error) {
    console.error('Error processing request:', error)
    return res.status(500).json({
      error: 'Failed to process request',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
  }
} 