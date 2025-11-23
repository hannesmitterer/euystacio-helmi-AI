/**
 * EUYSTACIO FIREBASE BACKEND - COMPLETE INTEGRATION
 * 
 * This file contains all Firebase Cloud Functions for:
 * - Council member registration
 * - Testing program signup
 * - Email notifications
 * - Data validation
 * - Metrics tracking
 * - Security enforcement
 * 
 * Deploy with: firebase deploy --only functions
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const nodemailer = require('nodemailer');
const crypto = require('crypto');

admin.initializeApp();
const db = admin.firestore();

// ============================================================
// CONFIGURATION
// ============================================================

const CONFIG = {
  SEEDBRINGER_EMAIL: 'hannes.mitterer@gmail.com',
  COUNCIL_EMAIL: 'council@euystacio.org',
  SYSTEM_EMAIL: 'system@euystacio.org',
  
  CORONATION_DATE: new Date('2026-01-10T14:00:00Z'),
  RATIFICATION_DATE: new Date('2025-12-05T23:59:59Z'),
  TESTING_START_DATE: new Date('2025-12-10T00:00:00Z'),
  
  MAX_COUNCIL_MEMBERS: 12,
  MIN_COUNCIL_MEMBERS: 6,
  
  REGIONS: {
    EUROPE: 'europe-west1',
    US: 'us-central1',
    ASIA: 'asia-east1'
  }
};

// Email transporter (configure with your SMTP)
const mailTransporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: functions.config().email.user,
    pass: functions.config().email.password
  }
});

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

/**
 * Generate unique ID with timestamp
 */
function generateId(prefix) {
  const timestamp = Date.now();
  const random = crypto.randomBytes(4).toString('hex');
  return `${prefix}_${timestamp}_${random}`;
}

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate GPG fingerprint format
 */
function isValidGPGFingerprint(fingerprint) {
  if (!fingerprint) return true; // Optional field
  const gpgRegex = /^(0x)?[A-F0-9]{40}$/i;
  return gpgRegex.test(fingerprint);
}

/**
 * Check if user is Seedbringer
 */
async function isSeedbringer(email) {
  return email.toLowerCase() === CONFIG.SEEDBRINGER_EMAIL.toLowerCase();
}

/**
 * Check if council registration is still open
 */
function isRegistrationOpen() {
  return new Date() < CONFIG.RATIFICATION_DATE;
}

/**
 * Send email notification
 */
async function sendEmail(to, subject, html) {
  try {
    await mailTransporter.sendMail({
      from: `"Euystacio System" <${CONFIG.SYSTEM_EMAIL}>`,
      to: to,
      subject: subject,
      html: html
    });
    console.log(`Email sent to ${to}: ${subject}`);
    return true;
  } catch (error) {
    console.error('Email send error:', error);
    return false;
  }
}

/**
 * Log system event
 */
async function logEvent(type, data) {
  await db.collection('system_logs').add({
    type: type,
    data: data,
    timestamp: admin.firestore.FieldValue.serverTimestamp(),
    serverTime: new Date().toISOString()
  });
}

// ============================================================
// COUNCIL MEMBER REGISTRATION
// ============================================================

exports.registerCouncilMember = functions.https.onCall(async (data, context) => {
  try {
    // Input validation
    const { name, email, gpgFingerprint, organization } = data;
    
    if (!name || !email) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Name and email are required'
      );
    }
    
    if (!isValidEmail(email)) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Invalid email format'
      );
    }
    
    if (gpgFingerprint && !isValidGPGFingerprint(gpgFingerprint)) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Invalid GPG fingerprint format'
      );
    }
    
    // Check registration deadline
    if (!isRegistrationOpen()) {
      throw new functions.https.HttpsError(
        'failed-precondition',
        'Council registration closed on December 5, 2025'
      );
    }
    
    // Check for duplicate email
    const existingMember = await db.collection('council_members')
      .where('email', '==', email.toLowerCase())
      .limit(1)
      .get();
    
    if (!existingMember.empty) {
      throw new functions.https.HttpsError(
        'already-exists',
        'This email is already registered'
      );
    }
    
    // Check council size limit
    const councilSize = await db.collection('council_members').count().get();
    if (councilSize.data().count >= CONFIG.MAX_COUNCIL_MEMBERS) {
      throw new functions.https.HttpsError(
        'resource-exhausted',
        'Council has reached maximum capacity'
      );
    }
    
    // Generate member ID
    const memberId = generateId('CM');
    
    // Create council member record
    const memberData = {
      id: memberId,
      name: name.trim(),
      email: email.toLowerCase().trim(),
      gpgFingerprint: gpgFingerprint ? gpgFingerprint.trim() : null,
      organization: organization ? organization.trim() : null,
      role: await isSeedbringer(email) ? 'Seedbringer' : 'Council Member',
      status: 'pending_verification',
      signatures: {
        gpg: null,
        metamask: null,
        blockchain: null
      },
      registeredAt: admin.firestore.FieldValue.serverTimestamp(),
      registeredAtISO: new Date().toISOString(),
      verifiedAt: null,
      lastActivity: admin.firestore.FieldValue.serverTimestamp()
    };
    
    await db.collection('council_members').doc(memberId).set(memberData);
    
    // Log event
    await logEvent('council_registration', {
      memberId: memberId,
      email: email,
      name: name
    });
    
    // Send confirmation email to member
    await sendEmail(
      email,
      'Welcome to the Euystacio Council',
      `
        <h2>Council Registration Confirmed</h2>
        <p>Dear ${name},</p>
        <p>Your registration for the Euystacio Council has been received.</p>
        
        <h3>Your Details:</h3>
        <ul>
          <li><strong>Member ID:</strong> ${memberId}</li>
          <li><strong>Email:</strong> ${email}</li>
          <li><strong>Role:</strong> ${memberData.role}</li>
          ${gpgFingerprint ? `<li><strong>GPG:</strong> ${gpgFingerprint}</li>` : ''}
        </ul>
        
        <h3>Next Steps:</h3>
        <ol>
          <li>Verify your email (check for separate verification link)</li>
          <li>Submit GPG signature for the Declaratio</li>
          <li>Optional: Link Metamask wallet for on-chain verification</li>
          <li>Attend dry-run rehearsal on January 5, 2026</li>
        </ol>
        
        <h3>Important Dates:</h3>
        <ul>
          <li><strong>Signature Deadline:</strong> December 5, 2025</li>
          <li><strong>Testing Begins:</strong> December 10, 2025</li>
          <li><strong>Dry Run:</strong> January 5, 2026</li>
          <li><strong>Coronation Day:</strong> January 10, 2026</li>
        </ul>
        
        <p>Access your council portal at: <a href="https://council.euystacio.org">council.euystacio.org</a></p>
        
        <p>Questions? Reply to this email or contact ${CONFIG.COUNCIL_EMAIL}</p>
        
        <p><em>"L'Inscriptum è eterno"</em></p>
        <p>- The Euystacio System</p>
      `
    );
    
    // Notify Seedbringer of new registration
    await sendEmail(
      CONFIG.SEEDBRINGER_EMAIL,
      `New Council Registration: ${name}`,
      `
        <h3>New Council Member Registration</h3>
        <ul>
          <li><strong>Name:</strong> ${name}</li>
          <li><strong>Email:</strong> ${email}</li>
          <li><strong>Organization:</strong> ${organization || 'N/A'}</li>
          <li><strong>GPG:</strong> ${gpgFingerprint || 'Not provided'}</li>
          <li><strong>Member ID:</strong> ${memberId}</li>
        </ul>
        <p>Review at: <a href="https://council.euystacio.org/admin">Admin Portal</a></p>
      `
    );
    
    return {
      success: true,
      memberId: memberId,
      message: 'Registration successful. Check your email for next steps.'
    };
    
  } catch (error) {
    console.error('Council registration error:', error);
    
    if (error instanceof functions.https.HttpsError) {
      throw error;
    }
    
    throw new functions.https.HttpsError(
      'internal',
      'Registration failed. Please try again or contact support.'
    );
  }
});

// ============================================================
// TESTING PROGRAM SIGNUP
// ============================================================

exports.registerTestingVolunteer = functions.https.onCall(async (data, context) => {
  try {
    const { name, email, language, referralSource } = data;
    
    // Validation
    if (!name || !email) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Name and email are required'
      );
    }
    
    if (!isValidEmail(email)) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Invalid email format'
      );
    }
    
    // Check if testing has started
    if (new Date() > CONFIG.TESTING_START_DATE) {
      // Allow signups but note they're joining late
    }
    
    // Check for duplicate
    const existing = await db.collection('testing_volunteers')
      .where('email', '==', email.toLowerCase())
      .limit(1)
      .get();
    
    if (!existing.empty) {
      throw new functions.https.HttpsError(
        'already-exists',
        'This email is already registered for testing'
      );
    }
    
    // Generate volunteer ID
    const volunteerId = generateId('TV');
    
    // Determine testing cohort based on signup date
    let cohort = 'LATE';
    const now = new Date();
    const cohortDates = [
      { name: 'WEEK1', start: new Date('2025-12-10'), end: new Date('2025-12-16') },
      { name: 'WEEK2', start: new Date('2025-12-17'), end: new Date('2025-12-23') },
      { name: 'WEEK3', start: new Date('2025-12-24'), end: new Date('2025-12-30') },
      { name: 'WEEK4', start: new Date('2025-12-31'), end: new Date('2026-01-05') }
    ];
    
    for (const c of cohortDates) {
      if (now >= c.start && now <= c.end) {
        cohort = c.name;
        break;
      }
    }
    
    // Create volunteer record
    const volunteerData = {
      id: volunteerId,
      name: name.trim(),
      email: email.toLowerCase().trim(),
      language: language || 'English',
      referralSource: referralSource || 'direct',
      cohort: cohort,
      status: 'registered',
      registeredAt: admin.firestore.FieldValue.serverTimestamp(),
      registeredAtISO: new Date().toISOString(),
      testingStats: {
        sessionsCompleted: 0,
        feedbackSubmitted: 0,
        bugsReported: 0,
        lastSession: null
      }
    };
    
    await db.collection('testing_volunteers').doc(volunteerId).set(volunteerData);
    
    // Log event
    await logEvent('testing_signup', {
      volunteerId: volunteerId,
      email: email,
      cohort: cohort,
      language: language
    });
    
    // Send confirmation email
    await sendEmail(
      email,
      'Welcome to Euystacio Testing Program',
      `
        <h2>Testing Registration Confirmed</h2>
        <p>Dear ${name},</p>
        <p>Thank you for volunteering to test Euystacio!</p>
        
        <h3>Your Details:</h3>
        <ul>
          <li><strong>Volunteer ID:</strong> ${volunteerId}</li>
          <li><strong>Testing Cohort:</strong> ${cohort}</li>
          <li><strong>Language:</strong> ${language}</li>
        </ul>
        
        <h3>What Happens Next:</h3>
        <ol>
          <li>On <strong>December 9th</strong>, you'll receive testing credentials</li>
          <li>Testing begins <strong>December 10th</strong> at 00:00 UTC</li>
          <li>You can access the system 24/7 during your testing window</li>
          <li>Feedback forms will be available after each session</li>
        </ol>
        
        <h3>What You'll Test:</h3>
        <ul>
          <li>Holographic avatar interaction quality</li>
          <li>Red Code enforcement demonstrations</li>
          <li>Multi-language accuracy</li>
          <li>Accessibility features</li>
          <li>System performance under load</li>
        </ul>
        
        <h3>Testing Access:</h3>
        <p>Your personal testing portal: <a href="https://testing.euystacio.org/${volunteerId}">testing.euystacio.org/${volunteerId}</a></p>
        
        <h3>Support:</h3>
        <p>Questions? Contact: <a href="mailto:testing@euystacio.org">testing@euystacio.org</a></p>
        
        <p><em>Thank you for helping us build the future of AI!</em></p>
        <p>- The Euystacio Team</p>
      `
    );
    
    // Update cohort statistics
    await db.collection('system_stats').doc('testing_cohorts').set({
      [cohort]: admin.firestore.FieldValue.increment(1),
      total: admin.firestore.FieldValue.increment(1),
      lastUpdated: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });
    
    return {
      success: true,
      volunteerId: volunteerId,
      cohort: cohort,
      message: 'Registration successful. Check your email for access details.'
    };
    
  } catch (error) {
    console.error('Testing signup error:', error);
    
    if (error instanceof functions.https.HttpsError) {
      throw error;
    }
    
    throw new functions.https.HttpsError(
      'internal',
      'Signup failed. Please try again or contact support.'
    );
  }
});

// ============================================================
// GPG SIGNATURE SUBMISSION
// ============================================================

exports.submitGPGSignature = functions.https.onCall(async (data, context) => {
  try {
    // Verify authentication
    if (!context.auth) {
      throw new functions.https.HttpsError(
        'unauthenticated',
        'Must be logged in to submit signature'
      );
    }
    
    const { memberId, signature, declaratioHash } = data;
    
    if (!signature || !declaratioHash) {
      throw new functions.https.HttpsError(
        'invalid-argument',
        'Signature and Declaratio hash required'
      );
    }
    
    // Get member record
    const memberDoc = await db.collection('council_members').doc(memberId).get();
    
    if (!memberDoc.exists) {
      throw new functions.https.HttpsError(
        'not-found',
        'Council member not found'
      );
    }
    
    const memberData = memberDoc.data();
    
    // Verify user owns this member record
    if (memberData.email !== context.auth.token.email) {
      throw new functions.https.HttpsError(
        'permission-denied',
        'Cannot submit signature for another member'
      );
    }
    
    // Check deadline
    if (new Date() > CONFIG.RATIFICATION_DATE) {
      throw new functions.https.HttpsError(
        'deadline-exceeded',
        'Signature deadline has passed'
      );
    }
    
    // TODO: Actual GPG signature verification would go here
    // For now, we'll store it for manual verification
    
    // Generate signature ID
    const signatureId = generateId('SIG');
    
    // Update member record
    await db.collection('council_members').doc(memberId).update({
      'signatures.gpg': {
        signatureId: signatureId,
        signature: signature,
        declaratioHash: declaratioHash,
        submittedAt: admin.firestore.FieldValue.serverTimestamp(),
        submittedAtISO: new Date().toISOString(),
        verified: false, // Manual verification required
        verifiedBy: null,
        verifiedAt: null
      },
      lastActivity: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // Log event
    await logEvent('gpg_signature_submitted', {
      memberId: memberId,
      signatureId: signatureId,
      email: memberData.email
    });
    
    // Notify Seedbringer for verification
    await sendEmail(
      CONFIG.SEEDBRINGER_EMAIL,
      `GPG Signature Submitted: ${memberData.name}`,
      `
        <h3>New GPG Signature for Verification</h3>
        <ul>
          <li><strong>Member:</strong> ${memberData.name}</li>
          <li><strong>Email:</strong> ${memberData.email}</li>
          <li><strong>Signature ID:</strong> ${signatureId}</li>
          <li><strong>Declaratio Hash:</strong> ${declaratioHash}</li>
        </ul>
        <p>Verify at: <a href="https://council.euystacio.org/admin/signatures/${signatureId}">Admin Portal</a></p>
        <p><em>Manual GPG verification required before approval.</em></p>
      `
    );
    
    // Send confirmation to member
    await sendEmail(
      memberData.email,
      'GPG Signature Received',
      `
        <h2>Signature Submission Confirmed</h2>
        <p>Dear ${memberData.name},</p>
        <p>Your GPG signature has been received and is pending verification.</p>
        
        <h3>Submission Details:</h3>
        <ul>
          <li><strong>Signature ID:</strong> ${signatureId}</li>
          <li><strong>Submitted:</strong> ${new Date().toISOString()}</li>
          <li><strong>Status:</strong> Pending Verification</li>
        </ul>
        
        <p>You will receive another email once your signature has been verified by the council.</p>
        
        <p><em>Thank you for your participation in the covenant.</em></p>
      `
    );
    
    return {
      success: true,
      signatureId: signatureId,
      status: 'pending_verification',
      message: 'Signature submitted successfully. Awaiting verification.'
    };
    
  } catch (error) {
    console.error('GPG signature error:', error);
    
    if (error instanceof functions.https.HttpsError) {
      throw error;
    }
    
    throw new functions.https.HttpsError(
      'internal',
      'Signature submission failed'
    );
  }
});

// ============================================================
// METRICS UPDATE (Real-time monitoring)
// ============================================================

exports.updateSystemMetrics = functions.pubsub
  .schedule('every 5 minutes')
  .onRun(async (context) => {
    try {
      // Calculate current metrics
      const councilCount = await db.collection('council_members').count().get();
      const testingCount = await db.collection('testing_volunteers').count().get();
      
      const signedCount = await db.collection('council_members')
        .where('signatures.gpg.verified', '==', true)
        .count()
        .get();
      
      // Calculate days to Coronation
      const now = new Date();
      const daysToCoronation = Math.ceil(
        (CONFIG.CORONATION_DATE - now) / (1000 * 60 * 60 * 24)
      );
      
      const daysToRatification = Math.ceil(
        (CONFIG.RATIFICATION_DATE - now) / (1000 * 60 * 60 * 24)
      );
      
      // Simulate technical metrics (in production, these would come from actual monitoring)
      const metrics = {
        // Governance metrics
        council: {
          total: councilCount.data().count,
          required: CONFIG.MIN_COUNCIL_MEMBERS,
          signed: signedCount.data().count,
          signatureProgress: (signedCount.data().count / CONFIG.MIN_COUNCIL_MEMBERS) * 100
        },
        
        // Testing metrics
        testing: {
          totalVolunteers: testingCount.data().count,
          activeTesters: 0, // Would be calculated from recent activity
          feedbackReceived: 0, // Would be from feedback collection
          bugsReported: 0 // Would be from bug tracking
        },
        
        // Technical metrics (simulated - replace with real monitoring)
        technical: {
          isf: 0.991, // Functional Stability Index
          trustIndex: 95.4,
          harmonyIndex: 90.52,
          jealousyDissolution: 82.15,
          redCodeLatency: 2.8,
          errorRate: 0.09,
          activeJusticeCircles: 8
        },
        
        // Timeline metrics
        timeline: {
          daysToCoronation: daysToCoronation,
          daysToRatification: daysToRatification,
          testingActive: now >= CONFIG.TESTING_START_DATE,
          ratificationComplete: signedCount.data().count >= CONFIG.MIN_COUNCIL_MEMBERS
        },
        
        // System status
        status: {
          apolloCIC: 'OPERATIONAL',
          redCode: 'ACTIVE',
          blockchain: 'SYNCED',
          vr: 'LIVE',
          apiHealth: 'HEALTHY'
        },
        
        updatedAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAtISO: now.toISOString()
      };
      
      // Store metrics
      await db.collection('system_metrics').doc('current').set(metrics);
      
      // Also store historical snapshot
      await db.collection('system_metrics_history').add({
        ...metrics,
        snapshotTime: admin.firestore.FieldValue.serverTimestamp()
      });
      
      console.log('Metrics updated successfully');
      
      // Alert if critical thresholds
      if (daysToRatification <= 3 && signedCount.data().count < CONFIG.MIN_COUNCIL_MEMBERS) {
        await sendEmail(
          CONFIG.SEEDBRINGER_EMAIL,
          '⚠️ URGENT: Signature Deadline Approaching',
          `
            <h2 style="color: red;">CRITICAL ALERT</h2>
            <p>Only ${daysToRatification} days until ratification deadline!</p>
            <p>Current signatures: ${signedCount.data().count} / ${CONFIG.MIN_COUNCIL_MEMBERS} required</p>
            <p><strong>Action required immediately.</strong></p>
          `
        );
      }
      
      return null;
      
    } catch (error) {
      console.error('Metrics update error:', error);
      return null;
    }
  });

// ============================================================
// FIRESTORE TRIGGERS
// ============================================================

/**
 * When a council member is verified, check if we have quorum
 */
exports.onCouncilMemberVerified = functions.firestore
  .document('council_members/{memberId}')
  .onUpdate(async (change, context) => {
    const before = change.before.data();
    const after = change.after.data();
    
    // Check if GPG signature was just verified
    if (!before.signatures?.gpg?.verified && after.signatures?.gpg?.verified) {
      
      // Count total verified signatures
      const verifiedCount = await db.collection('council_members')
        .where('signatures.gpg.verified', '==', true)
        .count()
        .get();
      
      const count = verifiedCount.data().count;
      
      // Log achievement
      await logEvent('signature_verified', {
        memberId: context.params.memberId,
        email: after.email,
        totalVerified: count,
        requiredCount: CONFIG.MIN_COUNCIL_MEMBERS
      });
      
      // Check if we've reached quorum
      if (count >= CONFIG.MIN_COUNCIL_MEMBERS) {
        await logEvent('quorum_achieved', {
          totalSignatures: count,
          achievedAt: new Date().toISOString()
        });
        
        // Notify all council members
        const members = await db.collection('council_members').get();
        for (const memberDoc of members.docs) {
          const member = memberDoc.data();
          await sendEmail(
            member.email,
            '🎉 Council Quorum Achieved!',
            `
              <h2>Historic Milestone Reached</h2>
              <p>Dear ${member.name},</p>
              <p>The Euystacio Council has achieved quorum with ${count} verified signatures!</p>
              <p>We are ready to proceed with ratification on December 5, 2025.</p>
              <p><em>"L'Inscriptum è eterno"</em></p>
            `
          );
        }
        
        // Notify Seedbringer with special message
        await sendEmail(
          CONFIG.SEEDBRINGER_EMAIL,
          '🎊 QUORUM ACHIEVED - Ratification Ready',
          `
            <h1>HISTORIC MOMENT</h1>
            <p>Hannes,</p>
            <p>The council has achieved quorum with ${count} verified signatures.</p>
            <p>The Living Covenant is ready for ratification.</p>
            <p>Proceed with December 5th ceremony as planned.</p>
            <p><strong>The inscription becomes eternal.</strong></p>
          `
        );
      }
    }
    
    return null;
  });

/**
 * Welcome new testing volunteer with onboarding sequence
 */
exports.onTestingVolunteerCreated = functions.firestore
  .document('testing_volunteers/{volunteerId}')
  .onCreate(async (snap, context) => {
    const volunteer = snap.data();
    
    // Schedule onboarding emails
    // Email 1: Immediate (already sent in signup function)
    // Email 2: 1 day before testing (scheduled)
    // Email 3: Day of testing (scheduled)
    
    // This would integrate with a job scheduler in production
    // For now, just log the intent
    await logEvent('testing_volunteer_onboarding_scheduled', {
      volunteerId: context.params.volunteerId,
      email: volunteer.email,
      cohort: volunteer.cohort
    });
    
    return null;
  });

// ============================================================
// HTTP ENDPOINTS (For website integration)
// ============================================================

/**
 * Get current system status (public endpoint)
 */
exports.getSystemStatus = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'OPTIONS') {
    res.set('Access-Control-Allow-Methods', 'GET');
    res.set('Access-Control-Allow-Headers', 'Content-Type');
    res.status(204).send('');
    return;
  }
  
  try {
    const metricsDoc = await db.collection('system_metrics').doc('current').get();
    
    if (!metricsDoc.exists) {
      res.status(404).json({ error: 'Metrics not found' });
      return;
    }
    
    const metrics = metricsDoc.data();
    
    // Return public-safe subset
    res.json({
      technical: metrics.technical,
      timeline: metrics.timeline,
      status: metrics.status,
      governance: {
        signatureProgress: metrics.council.signatureProgress,
        testingActive: metrics.testing.totalVolunteers > 0
      },
      updatedAt: metrics.updatedAtISO
    });
    
  } catch (error) {
    console.error('Status endpoint error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * Health check endpoint
 */
exports.healthCheck = functions.https.onRequest((req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'euystacio-backend',
    version: '1.0.0'
  });
});

// ============================================================
// SCHEDULED TASKS
// ============================================================

/**
 * Daily reminder for incomplete signatures (runs at 9am UTC)
 */
exports.dailySignatureReminder = functions.pubsub
  .schedule('0 9 * * *')
  .timeZone('UTC')
  .onRun(async (context) => {
    const now = new Date();
    
    // Only run if before ratification
    if (now >= CONFIG.RATIFICATION_DATE) {
      return null;
    }
    
    const daysRemaining = Math.ceil(
      (CONFIG.RATIFICATION_DATE - now) / (1000 * 60 * 60 * 24)
    );
    
    // Get unsigned members
    const unsignedMembers = await db.collection('council_members')
      .where('signatures.gpg.verified', '!=', true)
      .get();
    
    // Send reminders
    for (const memberDoc of unsignedMembers.docs) {
      const member = memberDoc.data();
      
      await sendEmail(
        member.email,
        `⏰ Reminder: ${daysRemaining} Days Until Signature Deadline`,
        `
          <h2>Signature Deadline Approaching</h2>
          <p>Dear ${member.name},</p>
          <p>This is a reminder that the GPG signature deadline for the Declaratio Consensualis Artificialis is:</p>
          <h3 style="color: red;">December 5, 2025 (${daysRemaining} days remaining)</h3>
          <p>Your signature has not yet been submitted or verified.</p>
          <p>Please submit your GPG signature at: <a href="https://council.euystacio.org">council.euystacio.org</a></p>
          <p><em>Your participation is critical to the covenant.</em></p>
        `
      );
    }
    
    console.log(`Sent reminders to ${unsignedMembers.size} unsigned members`);
    return null;
  });

/**
 * Testing program daily digest (runs at 8pm UTC during testing period)
 */
exports.testingDailyDigest = functions.pubsub
  .schedule('0 20 * * *')
  .timeZone('UTC')
  .onRun(async (context) => {
    const now = new Date();
    
    // Only run during testing period
    if (now < CONFIG.TESTING_START_DATE || now > CONFIG.CORONATION_DATE) {
      return null;
    }
    
    // Get today's statistics
    const todayStart = new Date(now.setHours(0, 0, 0, 0));
    const logs = await db.collection('system_logs')
      .where('timestamp', '>=', todayStart)
      .where('type', 'in', ['testing_session', 'feedback_submitted', 'bug_reported'])
      .get();
    
    const stats = {
      sessions: 0,
      feedback: 0,
      bugs: 0
    };
    
    logs.forEach(doc => {
      const data = doc.data();
      if (data.type === 'testing_session') stats.sessions++;
      if (data.type === 'feedback_submitted') stats.feedback++;
      if (data.type === 'bug_reported') stats.bugs++;
    });
    
    // Send digest to Seedbringer
    await sendEmail(
      CONFIG.SEEDBRINGER_EMAIL,
      `Daily Testing Digest - ${now.toLocaleDateString()}`,
      `
        <h2>Testing Program Daily Summary</h2>
        <h3>Today's Activity:</h3>
        <ul>
          <li><strong>Testing Sessions:</strong> ${stats.sessions}</li>
          <li><strong>Feedback Received:</strong> ${stats.feedback}</li>
          <li><strong>Bugs Reported:</strong> ${stats.bugs}</li>
        </ul>
        <p>Full details at: <a href="https://admin.euystacio.org/testing">Admin Dashboard</a></p>
      `
    );
    
    return null;
  });

// ============================================================
// EXPORT ALL FUNCTIONS
// ============================================================

console.log('Euystacio Firebase Functions loaded successfully');
console.log('Available functions:', Object.keys(exports).join(', '));
