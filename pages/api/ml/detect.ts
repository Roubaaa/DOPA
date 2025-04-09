import type { NextApiRequest, NextApiResponse } from 'next'
import formidable, { Fields, Files, File } from 'formidable'
import fs from 'fs'
import path from 'path'
import { promisify } from 'util'
import FormData from 'form-data'
import fetch from 'node-fetch'

// Get Python backend URL from environment variable
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:5000/api/detect'

export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  let tempFilePath: string | null = null

  try {
    console.log('Starting ML processing...')
    
    const form = formidable({ 
      keepExtensions: true,
      maxFileSize: 10 * 1024 * 1024, // 10MB max
    })

    const [fields, files] = await new Promise<[Fields, Files]>((resolve, reject) => {
      form.parse(req, (err: Error | null, fields: Fields, files: Files) => {
        if (err) reject(err)
        resolve([fields, files])
      })
    })

    console.log('Parsed form data:', { fields, files })

    const fileArray = files.image as File[]
    if (!fileArray || fileArray.length === 0) {
      console.error('No image file provided')
      return res.status(400).json({ error: 'No image file provided' })
    }
    
    const file = fileArray[0]
    tempFilePath = file.filepath
    console.log('Processing file:', { 
      path: tempFilePath,
      size: file.size,
      type: file.mimetype
    })

    // Create form data
    const formData = new FormData()
    formData.append('image', fs.createReadStream(tempFilePath), {
      filename: file.originalFilename || 'image.jpg',
      contentType: file.mimetype || 'image/jpeg'
    })

    console.log('Sending request to Python backend at:', PYTHON_BACKEND_URL)
    
    // Send to Python backend
    const response = await fetch(PYTHON_BACKEND_URL, {
      method: 'POST',
      body: formData,
      headers: formData.getHeaders()
    })

    console.log('Python backend response status:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Python backend error:', errorText)
      let errorMessage = 'Failed to process image'
      try {
        const errorJson = JSON.parse(errorText)
        errorMessage = errorJson.error || errorMessage
        if (errorJson.details) {
          errorMessage += `: ${errorJson.details}`
        }
      } catch (e) {
        // If we can't parse the error as JSON, use the raw text
        errorMessage = errorText
      }
      throw new Error(errorMessage)
    }

    const results = await response.json()
    console.log('Successfully processed image')
    return res.status(200).json(results)

  } catch (error) {
    console.error('Error processing image:', error)
    
    if (error instanceof Error && error.message.includes('ECONNREFUSED')) {
      return res.status(503).json({ 
        error: 'Python backend is not running.',
        details: 'Please start the Python backend service'
      })
    }
    
    return res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Failed to process image',
      details: error instanceof Error ? error.stack : 'Unknown error'
    })
  } finally {
    // Clean up temp file
    if (tempFilePath) {
      try {
        await promisify(fs.unlink)(tempFilePath)
        console.log('Cleaned up temp file:', tempFilePath)
      } catch (cleanupError) {
        console.error('Error cleaning up temp file:', cleanupError)
      }
    }
  }
} 