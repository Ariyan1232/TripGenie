import { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  Share,
} from 'react-native';
import { Colors } from '../constants/colors';
import Button from '../components/Button';
import Card from '../components/Card';
import { getTrip } from '../api/trips';

export default function MembersScreen({ navigation, route }) {
  const { tripId, tripName } = route.params;
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchTrip = async () => {
    try {
      const data = await getTrip(tripId);
      setTrip(data);
    } catch (error) {
      console.log('Error details:', error.message);
      Alert.alert('Error', `Could not create the trip. ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrip();
  }, []);

  const handleShare = async () => {
    try {
      await Share.share({
        message: `Join my trip on Converge! Trip code: ${tripId}`,
      });
    } catch (error) {
      Alert.alert('Error', 'Could not share trip code.');
    }
  };

  const handleRefresh = () => {
    setLoading(true);
    fetchTrip();
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={Colors.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>

        {/* Trip name */}
        <Text style={styles.tripName}>{trip?.name}</Text>
        <Text style={styles.subtitle}>
          {trip?.travelers?.length} traveler{trip?.travelers?.length !== 1 ? 's' : ''} so far
        </Text>

        {/* Trip code */}
        <Card style={styles.codeCard}>
          <Text style={styles.codeLabel}>TRIP CODE</Text>
          <Text style={styles.code}>{tripId}</Text>
          <Text style={styles.codeHint}>
            Share this code so others can join
          </Text>
          <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
            <Text style={styles.shareButtonText}>Share trip code</Text>
          </TouchableOpacity>
        </Card>

        {/* Members list */}
        <Text style={styles.sectionLabel}>WHO'S IN</Text>

        {trip?.travelers?.map((traveler, index) => (
          <Card key={traveler.id}>
            <View style={styles.memberRow}>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>
                  {traveler.name[0].toUpperCase()}
                </Text>
              </View>
              <View style={styles.memberInfo}>
                <Text style={styles.memberName}>{traveler.name}</Text>
                <Text style={styles.memberDetail}>
                  Flying from {traveler.origin_airport}
                </Text>
                <Text style={styles.memberDetail}>
                  {traveler.earliest_departure} → {traveler.latest_return}
                </Text>
                {traveler.destination_votes.length > 0 && (
                  <Text style={styles.memberVotes}>
                    Votes: {traveler.destination_votes.join(', ')}
                  </Text>
                )}
              </View>
              {index === 0 && (
                <Text style={styles.organizerBadge}>Organizer</Text>
              )}
            </View>
          </Card>
        ))}

        {/* Actions */}
        <View style={styles.actions}>
          <Button
            title="Refresh members"
            variant="secondary"
            onPress={handleRefresh}
          />
          <View style={styles.gap} />
          <Button
            title="View flight results"
            onPress={() => navigation.navigate('Results', { tripId })}
          />
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  container: {
    padding: 24,
    paddingBottom: 48,
  },
  tripName: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.textDark,
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 15,
    color: Colors.textMuted,
    marginTop: 4,
    marginBottom: 24,
  },
  codeCard: {
    alignItems: 'center',
    paddingVertical: 20,
    marginBottom: 24,
  },
  codeLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 1,
    marginBottom: 8,
  },
  code: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.primary,
    letterSpacing: 4,
    marginBottom: 8,
  },
  codeHint: {
    fontSize: 13,
    color: Colors.textMuted,
    marginBottom: 16,
  },
  shareButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: Colors.primary,
  },
  shareButtonText: {
    color: Colors.primary,
    fontWeight: '600',
    fontSize: 14,
  },
  sectionLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 1,
    marginBottom: 12,
  },
  memberRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  avatarText: {
    color: Colors.white,
    fontWeight: '700',
    fontSize: 16,
  },
  memberInfo: {
    flex: 1,
    gap: 2,
  },
  memberName: {
    fontSize: 15,
    fontWeight: '600',
    color: Colors.textDark,
  },
  memberDetail: {
    fontSize: 13,
    color: Colors.textMuted,
  },
  memberVotes: {
    fontSize: 13,
    color: Colors.primary,
    marginTop: 2,
  },
  organizerBadge: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.primary,
    backgroundColor: '#EBF0F7',
    paddingVertical: 3,
    paddingHorizontal: 8,
    borderRadius: 6,
  },
  actions: {
    marginTop: 32,
  },
  gap: {
    height: 12,
  },
});